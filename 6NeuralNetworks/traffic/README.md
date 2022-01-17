The accuracy of the code was only 5% when apllied a dropout of 50%. When the code for dropout was removed the accuracy
went all the way upto 94%!! So, this indicated that the input will be much more familiar to the trained model, however
removing the dropout completely is not viable(obviously) and also decrease in dropout value results in higher training
time. I then tried adding multiple hidden layers, which gave an impressive accuracy for lower dropout values (94%);
however the best outcome was one when I added a secondary Convolution and Pooling when it resulted an accuracy of 97%.
Alas this outcome wasn't consistent; but on adding another hidden layer the output got quite stable.
