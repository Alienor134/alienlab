from statsmodels.regression import linear_model
from statsmodels.api import add_constant
from scipy.interpolate import InterpolatedUnivariateSpline
import numpy as np
import warnings
"""
Example of use:

N = 10
frequencies = 10**np.linspace(-3.5, 2, N)
radius, phase, all_outputs, sin_lo, cos_lo = bode.bode_diagram(frequencies, signal_12, 200)

pulse = frequencies * 2 * np.pi
x0 = [0.1, 0.1, 0]

parameters_estimated = optimize.least_squares(utils.regression_func.residuals,  x0, bounds = (-1e5,1e5),
                                    args = (pulse, radius[:,2], utils.regression_func.low_pass)).x
y =  utils.regression_func.low_pass(parameters_estimated, pulse)
plt.close('all')
fig = plt.figure()
ax = plt.gca()
ax.scatter(pulse, radius[:,2])
ax.plot(pulse, y[::-1])
ax.set_xscale('log')
plt.xlabel('frequencies (rad/s)')
plt.ylabel('amplitude locked-in')
plt.title('cut-off tau %0.3f'%parameters_estimated[1])
bode.p.saving(fig)
plt.show()
"""



def get_func(X, Y, k = 3):
        Y = np.array([y for x, y in sorted(zip(X, Y))]) #preliminary sorting of the arrays along wavelength 
                                                            #(in case the graph in not properly ordered)
        X = np.sort(X)
        func = InterpolatedUnivariateSpline(X, Y, k=k) # interpolate given values with step 1 nm
        return func



def get_polyfit_func(X, Y, order):
    func = np.poly1d(np.polyfit(X, Y, order))
    return func


def get_affine_func(X, Y):
    warnings.filterwarnings('ignore')
    Yreg, a, b, sum = regression_affine(X, Y)
    return lambda x: a*x + b

    
def regression_affine(X, Y, details = True):
        Xreg = add_constant(X) #Add a constant to fit tan affine model

        model = linear_model.OLS(Y, Xreg) #Linear regression
        results = model.fit()
        [b, a] = results.params #parameters of the affine curve
        Yreg = a*X + b #regression curve

        return Yreg, a, b, results

def get_linear_func(X, Y):
    warnings.filterwarnings('ignore')
    Yreg, a, sum = regression_linear(X, Y)
    return lambda x: a*x

def regression_linear(X, Y, details = True):

        model = linear_model.OLS(Y, X) #Linear regression
        results = model.fit()
        a = results.params #parameters of the affine curve
        Yreg = a*X #regression curve

        return Yreg, a, results



def exp_decay(parameters,xdata):
    '''
    Calculate an exponetial decay of the form:
    S= a * exp(-xdata/b)
    '''
    A = parameters[0]
    tau = parameters[1]
    y0 = parameters[2]
    return A * np.exp(-xdata/tau) + y0

def band_pass(parameters, xdata):
    
    H = parameters[0]
    tau = parameters[1]
    a0 = parameters[2]
    
    return H * (xdata * tau) /(1 + (xdata  * tau)**2) + a0

def low_pass(parameters, xdata):
    
    H = parameters[0]
    tau = parameters[1]
    a0 = parameters[2]
    
    return H*(xdata * tau)**2 /(1 + (xdata * tau)**2) + a0

def high_pass(parameters, xdata):
    
    H = parameters[0]
    tau = parameters[1]
    a0 = parameters[2]
    
    return H /(1 + (xdata * tau)**2) + a0


def platt(parameters, xdata):
    M = parameters[0]
    alpha = parameters[1]
    return M*(1- np.exp(-alpha*xdata/M))


def amplitude(parameters, xdata):
    
    H = parameters[0]
    tau = parameters[1]
    a0 = parameters[2]
    
    return (H /(1 + (xdata * tau)**2))**0.5 + a0

def residuals(parameters,x_data,y_observed,func):
    '''
    Compute residuals of y_predicted - y_observed
    where:
    y_predicted = func(parameters,x_data)
    '''
    return func(parameters,x_data) - y_observed
