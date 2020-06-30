from pydlm import dynamic
data = np.random.random((1, 100))
mydlm = dlm(data) + trend(degree=1, 0.98, name='a') +
                dynamic(features=[[i] for i in range(100)], 1, name='b')
mydlm.fit()
coef_a = mydlm.getLatentState('a')
coef_b = mydlm.getLatentState('b')