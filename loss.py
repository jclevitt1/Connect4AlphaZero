import tensorflow as tf

def softmax_cross_entropy_with_logits(y_true, y_pred):
    p = y_pred
    pi = y_true
    
    zero = tf.zeros(shape = tf.shape(pi), dtype = tf.float32)
    where = tf.equal(pi, zero)
    
    negs = tf.fill(tf.shape(pi), -100)
    p = tf.where(where, negs, p)
    
    loss = tf.nn.softmax_cross_entropy_with_logits(labels = pi, logits = p)
    
    return loss