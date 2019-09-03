import tensorflow as tf
import numpy as np
import joblib
import layers
import tensorflow.contrib.keras as K

def build_placeholders(info,config,batch_size=4):
    adj_channel_num=info.adj_channel_num
    placeholders = {
        'adjs':[[tf.sparse_placeholder(tf.float32,name="adj_"+str(a)+"_"+str(b)) for a in range(adj_channel_num)] for b in range(batch_size)],
        'nodes': tf.placeholder(tf.int32, shape=(batch_size,info.graph_node_num),name="node"),
        'labels': tf.placeholder(tf.float32, shape=(batch_size,info.label_dim),name="label"),
        'mask': tf.placeholder(tf.float32, shape=(batch_size,),name="mask"),
        'mask_label': tf.placeholder(tf.float32, shape=(batch_size,info.label_dim),name="mask_label"),
        'dropout_rate': tf.placeholder(tf.float32, name="dropout_rate"),
        'is_train': tf.placeholder(tf.bool, name="is_train"),
        'mask_node': tf.placeholder(tf.float32, shape=(batch_size,info.graph_node_num),name="mask_node"),
        'enabled_node_nums': tf.placeholder(tf.int32, shape=(batch_size,), name="enabled_node_nums"),
    }
    if info.feature_enabled:
        placeholders['features']=tf.placeholder(tf.float32, shape=(batch_size,info.graph_node_num,info.feature_dim),name="feature")
    else:
        placeholders['features']=None
    return  placeholders

def build_model(placeholders,info,config,batch_size=4):
    adj_channel_num=info.adj_channel_num
    embedding_dim=config["embedding_dim"]
    in_adjs=placeholders["adjs"]
    features=placeholders["features"]
    in_nodes=placeholders["nodes"]
    labels=placeholders["labels"]
    mask=placeholders["mask"]
    mask_label=placeholders["mask_label"]
    #dropout_rate=placeholders["dropout_rate"]
    dropout_rate=0.3
    is_train=placeholders["is_train"]
    mask_node=placeholders["mask_node"]
    enabled_node_nums=placeholders["enabled_node_nums"]

    layer=features
    input_dim=info.feature_dim
    with tf.variable_scope("rollout"):
        if features is None:
            layer=K.layers.Embedding(info.all_node_num,embedding_dim)(in_nodes)
            input_dim=embedding_dim
        # layer: batch_size x graph_node_num x dim
        layer=layers.GraphConv(128,adj_channel_num)(layer,adj=in_adjs)
        layer=layers.GraphBatchNormalization()(layer,
            max_node_num=info.graph_node_num,enabled_node_nums=enabled_node_nums)
        layer=tf.nn.relu(layer)
#       layer=K.layers.Dropout(dropout_rate)(layer)

        layer=layers.GraphConv(128,adj_channel_num)(layer,adj=in_adjs)
        layer=layers.GraphBatchNormalization()(layer,
            max_node_num=info.graph_node_num,enabled_node_nums=enabled_node_nums)
        layer=tf.nn.relu(layer)
#       layer=K.layers.Dropout(dropout_rate)(layer)

        layer=layers.GraphConv(128,adj_channel_num)(layer,adj=in_adjs)
        layer=layers.GraphBatchNormalization()(layer,
            max_node_num=info.graph_node_num,enabled_node_nums=enabled_node_nums)
        layer=tf.nn.relu(layer)
#       layer=K.layers.Dropout(dropout_rate)(layer)

        layer=layers.GraphDense(128)(layer)
        layer=tf.nn.relu(layer)
#       layer=K.layers.Dropout(dropout_rate)(layer)

        layer=layers.GraphGather()(layer)
        layer=K.layers.Dense(info.label_dim)(layer)
        prediction=tf.nn.softmax(layer,name="output")
        # computing cost and metrics
        cost=mask*tf.nn.softmax_cross_entropy_with_logits_v2(labels=labels,logits=layer)
        cost_opt=tf.reduce_mean(cost)
        metrics={}
        cost_sum=tf.reduce_sum(cost)
        correct_count=mask*tf.cast(tf.equal(tf.argmax(prediction,1), tf.argmax(labels,1)),tf.float32)
        metrics["correct_count"]=tf.reduce_sum(correct_count)
    return layer,prediction,cost_opt,cost_sum,metrics
