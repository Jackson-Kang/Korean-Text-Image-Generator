import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import tensorflow.contrib.slim as slim

from sys import path
from os import getcwd
import json
import logging
import os
import random

import numpy as np

path.append(getcwd() + "/modules")
from md_lstm import multi_dimensional_rnn_while_loop

logger = logging.getLogger(__name__)

img_width = 28
img_height = 28

window_size = [1, 1]
hidden_size =256
learning_rate = 0.01
batch_size = 40
channels = 1
steps = 0
epochs = 50
display_step = 1

num_of_output = 11

log_option = False


def data_provider(mode, x, y):
    mnist_data_path = './MNIST_data/' + mode + '_mnist_labels.npy'

    if (os.path.isfile(mnist_data_path)):
        y = np.load(mnist_data_path)
    else:
        y = label_convert(x, y)
        np.save(mnist_data_path, y)

    return y


def label_convert(mnist_x, mnist_y):
    # shapes of input that tossed from main function
    # 2D List -> num_of_img x pixels that are consist of image

    # label -> [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #          [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -1]           -1: background
    new_label = []

    for img_index in range(len(mnist_x)):
        y_index = np.where(mnist_y[img_index] == 1)

        for pixel_index in range(len(mnist_x[img_index])):
            pixel_label = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int8)
            if mnist_x[img_index][pixel_index] != 0:
                pixel_label[y_index] = 1
            else:
                pixel_label[-1] = 1

            new_label.append(pixel_label)

    new_label = np.array(new_label)

    new_label = np.reshape(new_label, [int(len(mnist_y)/batch_size), batch_size, img_height, img_width, channels, num_of_output])

    return new_label


def remove_label_background(preds, answer):

    reshaped_preds = np.reshape(preds, [batch_size, img_width*img_height*channels, num_of_output])
    reshaped_answer = np.reshape(answer, [batch_size, img_width*img_height*channels, num_of_output])

    truth_tabel_bg = np.where(reshaped_answer.argmax(axis=2) == 10)
    truth_tabel_num = np.where(reshaped_answer.argmax(axis=2) != 10)

    without_bg_answer = reshaped_answer[truth_tabel_num]
    without_bg_preds = reshaped_preds[truth_tabel_num]

    with_bg_answer = reshaped_answer[truth_tabel_bg]
    with_bg_preds = reshaped_preds[truth_tabel_bg]

    return without_bg_preds, without_bg_answer, with_bg_preds, with_bg_answer




def run():
    mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
    # x must be [batch, h, w, channels]

    x = tf.placeholder(tf.float32, [batch_size, img_height, img_width, channels])
    y = tf.placeholder(tf.float32, shape=[batch_size, img_height, img_width, channels, num_of_output])

    input_layer = tf.contrib.slim.fully_connected(inputs=x, num_outputs=channels, activation_fn=tf.tanh)

    first_rnn_out, _ = multi_dimensional_rnn_while_loop(rnn_size=hidden_size, input_data=input_layer,
                                                  sh=window_size, scope_n="layer1")

    '''
    second_rnn_out, _ = multi_dimensional_rnn_while_loop(rnn_size=hidden_size, input_data=input_layer,
                                                  sh=window_size, scope_n="layer2", dims=[1])

    third_rnn_out, _ = multi_dimensional_rnn_while_loop(rnn_size=hidden_size, input_data=input_layer,
                                                  sh=window_size, scope_n="layer3", dims=[2])

    reversed_input = tf.reverse(third_rnn_out, [1])

    forth_rnn_out, _ = multi_dimensional_rnn_while_loop(rnn_size=hidden_size, input_data=input_layer,
                                                  sh=window_size, scope_n="layer4", dims=[2])

    reversed_rnn_out = tf.reverse(forth_rnn_out, [1])

    summation = tf.add(tf.add(first_rnn_out, second_rnn_out), tf.add(third_rnn_out, reversed_rnn_out))
    '''

    output_layer = tf.contrib.slim.fully_connected(inputs=first_rnn_out, num_outputs=num_of_output, activation_fn=tf.tanh)

    softmax_output = tf.nn.softmax(output_layer)

    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=output_layer, labels=y))

    optimizer = tf.train.AdamOptimizer(learning_rate).minimize(loss)

    sess = tf.Session(config=tf.ConfigProto(log_device_placement=log_option))
    sess.run(tf.global_variables_initializer())
    # runs operation

    train_steps = int(mnist.train.num_examples / batch_size)
    test_steps = int(mnist.test.num_examples/batch_size)

    train_y = data_provider("train", mnist.train.images, mnist.train.labels)
    test_y = data_provider("test", mnist.test.images, mnist.test.labels)

    train_x = np.reshape(mnist.train.images, [train_steps, batch_size, img_height, img_width, channels])
    test_x = np.reshape(mnist.test.images,
                        [test_steps, batch_size, img_height, img_width, channels])


    list_index = list(range(0, train_steps))
    random.shuffle(list_index)

    writer = tf.summary.FileWriter("./tensorboard_logs/", sess.graph)

    for epoch in range(epochs):

        print("***** epoch ", epoch + 1, " *****")

        list_index = list(range(0, train_steps))
        random.shuffle(list_index)

        for i in range(train_steps):
            
            preds, answer, _, cost = sess.run([softmax_output, y, optimizer, loss], feed_dict={x: train_x[list_index[i]], y: train_y[list_index[i]]})

            #print(list_index[i])

            cost_summary = tf.summary.scalar("cost", cost)

            if i % display_step == 0:

                test_index = list(range(0, test_steps))
                random.shuffle(test_index)

                removed_background_preds, removed_background_answer, with_bg_preds, with_bg_answer = remove_label_background(preds, answer)


                removed_correct_prediction = tf.equal(tf.argmax(removed_background_preds, axis=1), tf.argmax(removed_background_answer, axis=1))
                correct_prediction = tf.equal(tf.argmax(tf.reshape(preds, [batch_size, img_width*img_height*channels, num_of_output]), axis = 2), tf.argmax(tf.reshape(answer, [batch_size, img_width*img_height*channels, num_of_output]), axis = 2))

                removed_accuracy = tf.reduce_max(tf.reduce_mean(tf.cast(removed_correct_prediction, tf.float32), axis = 0))
                accuracy = tf.reduce_max(tf.reduce_mean(tf.cast(correct_prediction, tf.float32), axis = 1))

                bg_correct_prediction = tf.equal(tf.argmax(with_bg_preds, axis=1), tf.argmax(with_bg_answer, axis=1))
                bg_accuracy =  tf.reduce_mean(tf.cast(bg_correct_prediction, tf.float32), axis = 0)

                removed_result_accuracy = removed_accuracy.eval({x: test_x[test_index[i % test_steps]], y: test_y[test_index[i % test_steps]]}, session=sess)
                result_accuracy = accuracy.eval({ x: test_x[test_index[i % test_steps]], y: test_y[test_index[i% test_steps]]}, session = sess)
                calculated_bg_accuracy = bg_accuracy.eval({x: test_x[test_index[i % test_steps]], y: test_y[test_index[i% test_steps]]}, session = sess)

                non_bg_acc_summary = tf.summary.scalar("Non-BG Acc (per batch)", removed_result_accuracy)
                bg_acc_summary = tf.summary.scalar("BG Acc (per batch)", calculated_bg_accuracy)
                overall_acc_summary = tf.summary.scalar("Overall Acc (per image)", result_accuracy)

                merged = tf.summary.merge([cost_summary, non_bg_acc_summary, bg_acc_summary, overall_acc_summary])
                summary_str = sess.run(merged)

                writer.add_summary(summary_str, i)

                
                print("  step:", '%04d' % i, "  cost=", "{:.9f}".format(cost),
                        "  Non-background Accuracy(per batch): ", "{:.9f}".format(removed_result_accuracy), "  Background Accuracy(per batch): ", "{:.9f}".format(calculated_bg_accuracy), "  Overall Accuracy(per image): ", "{:.9f}".format(result_accuracy))
                

    sess.close()


if __name__ == '__main__':
    run()

'''
    784개 픽셀에서 background를 예측한 경우 제거 후 숫자를 표현하는데 쓰인 pixel들과 비교해 equal 수행해서 accuracy 계산, 그리고 각 image 단위로 가장 정확도 높은 것을 argmax로 뽑아내기
    
'''
