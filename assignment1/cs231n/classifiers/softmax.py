import numpy as np
from random import shuffle

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  N = np.shape(X)[0]
  C = np.shape(W)[1]
  dsoft = np.zeros((N, C))
  scores = X.dot(W)
  for i in range(N):

    #scores[i] -= scores[i].max()
    e_sum = np.sum(np.exp(scores[i]))
    e_i = np.exp(scores[i, y[i]])
    p_i = e_i / e_sum #softmax
    loss += -np.log(p_i)

    dsoft[i, y[i]] = -1/p_i * (1/e_sum * e_i + e_i**2 * -1/(e_sum**2))
    #dsoft[i, y[i]] = p_i - 1 #pi - yi
    for c in range(C):
      if c != y[i]:
        e_c = np.exp(scores[i, c])
        dsoft[i, c] = (e_i * (-1/(e_sum**2)) * e_c) * - 1/(e_i/e_sum)
  loss /= N
  loss += reg * np.sum(W*W)

  dsoft /= N
  dW = X.T.dot(dsoft)
  dW += 2 * reg * W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)
  N = X.shape[0]
  scores = X.dot(W)
  e_sum = np.sum(np.exp(scores), axis=1) # N, 1
  e_i = np.exp(scores[range(N), y])
  p_i = e_i / e_sum
  loss = np.sum(np.log(p_i)*-1)


  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  e_i = e_i.reshape((N, 1))
  e_sum = e_sum.reshape((N, 1))
  e_c = np.exp(scores[range(N)])
  p_i = e_i / e_sum
  dscores = (e_i * (-1 / (e_sum ** 2)) * e_c) * - 1 / (e_i / e_sum)
  dscores[range(N), y] = (-1 / p_i * (1 / e_sum * e_i + e_i ** 2 * -1 / (e_sum ** 2))).reshape((N,))

  loss += reg * np.sum(W * W)
  loss /= N

  dscores /= N
  dW = X.T.dot(dscores)
  dW += 2 * reg * W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW

