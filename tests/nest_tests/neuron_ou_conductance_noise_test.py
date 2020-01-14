#
# neuron_ou_conductance_noise_test.py
#
# This file is part of NEST.
#
# Copyright (C) 2004 The NEST Initiative
#
# NEST is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# NEST is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NEST.  If not, see <http://www.gnu.org/licenses/>.

import nest
import numpy as np

try:
    import matplotlib
    import matplotlib.pyplot as plt
    TEST_PLOTS = True
except:
    TEST_PLOTS = False


record_from = ['g_noise_ex', 'g_noise_in']


def simulate_OU_noise_neuron(resolution):
	''' Simulates a single neuron with OU noise conductances.

	Parameters
	----------
	resolution : float
		Resolution of the NEST simulation

	Returns
	-------
	dict
		State of the multimeter, which is connected to the neuron.
	tuple
		Tuple with the NEST id of the simulated neuron

	'''
	seed = np.random.randint(0, 2**32-1)
	print('seed: {}'.format(seed))
	nest.SetKernelStatus({'resolution': resolution, 'grng_seed': seed, 'rng_seeds': [seed+1]})

	nest.Install('nestmlmodule')
	neuron = nest.Create('hh_cond_exp_destexhe_nestml')

	multi = nest.Create('multimeter', params={'withgid': True, 'withtime': True, 'record_from': record_from, 'interval': resolution})

	nest.Connect(multi, neuron)
	nest.Simulate(500000)
	return nest.GetStatus(multi)[0]['events'], neuron


def calc_statistics(state, neuron):
	''' Calculates statistics for the Ornstein-Uhlenbeck-noise conductances.

	Calculates the means and variances of the conductances and compares them
	with the expected means and variances

	Parameters
	----------
	state : dict
		The state of the multimeter which you get by calling nest.GetStatus(multimeter)[0]['events']
	neuron : tuple
		Tuple with the NEST id of the neuron with the OU noise conductances
	'''

	print('\n\n======== Noise Conductance Statistics ==============')
	times = state['times']

	# excitatory noise
	sigma_ex = nest.GetStatus(neuron, 'sigma_noise_ex')[0]
	mean_ex = nest.GetStatus(neuron, 'g_noise_ex0')[0]
	tau_ex = nest.GetStatus(neuron, 'tau_syn_ex')[0]
	var_ex = sigma_ex**2 / (2 / tau_ex)

	# inhibitory noise
	sigma_in = nest.GetStatus(neuron, 'sigma_noise_in')[0]
	mean_in = nest.GetStatus(neuron, 'g_noise_in0')[0]
	tau_in = nest.GetStatus(neuron, 'tau_syn_in')[0]
	var_in = sigma_in**2 / (2 / tau_in)

	# variances
	print('\n____variances_______________________________________')
	vex = np.var(state['g_noise_ex'])
	vin = np.var(state['g_noise_in'])
	vex_trgt = sigma_ex**2
	vin_trgt = sigma_in**2
	diff_perc_vex = np.abs(1 - vex / vex_trgt) * 100
	diff_perc_vin = np.abs(1 - vin / vin_trgt) * 100
	print('ex: {:.2f}\ttarget = {:.2f}\tdiff = {:.2f} ({:.2f}%)'.format(vex, vex_trgt, np.abs(vex - vex_trgt), diff_perc_vex))
	print('in: {:.2f}\ttarget = {:.2f}\tdiff = {:.2f} ({:.2f}%)'.format(vin, vin_trgt, np.abs(vin - vin_trgt), diff_perc_vin))
	assert diff_perc_vex < 1.
	assert diff_perc_vin < 1.

	# means
	print('\n____means___________________________________________')
	m_ex_data = np.mean(state['g_noise_ex'])
	m_in_data = np.mean(state['g_noise_in'])
	diff_perc_mex = np.abs(1 - m_ex_data / mean_ex) * 100
	diff_perc_min = np.abs(1 - m_in_data / mean_in) * 100
	print('ex: {:.2f}\ttarget = {:.2f}\tdiff = {:.2f} ({:.2f}%)'.format(m_ex_data, mean_ex, np.abs(m_ex_data - mean_ex), diff_perc_mex))
	print('in: {:.2f}\ttarget = {:.2f}\tdiff = {:.2f} ({:.2f}%)\n'.format(m_in_data, mean_in, np.abs(m_in_data - mean_in), diff_perc_min))
	assert diff_perc_mex < 1.
	assert diff_perc_min < 1.


def plot_results(state):
	''' Reproduces figures 2A and 2B from Destexhe et al. 2001.

	Produces a plot with the time courses of the total excitatory (top left)
	and total inhibitory (bottom left) conductances during synaptic background
	activity as subplots. The two other subplots consist of distributions of 
	values for each conductance (excitatory and inhibitory).

	Parameters
	----------
	state : dict
		The state of the multimeter which you get by calling nest.GetStatus(multimeter)[0]['events']
	'''
	times = state['times']
	fig, ax = plt.subplots(2, 2, constrained_layout=True, figsize=(15, 10))
	mask = times <= 1200.
	for idx, rf in enumerate(record_from):
			ax_cond = ax[idx][0]
			ax_hist = ax[idx][1]

			if 'ex' in rf:
				ax_cond.set_ylim(0, 0.04)
				ax_cond.set_title('Excitatory Conductance')
				ax_hist.set_title('Conductance distribution (excitatory)')
			else:
				ax_cond.set_ylim(0.03, 0.08)
				ax_cond.set_title('Inhibitory Conductance')
				ax_hist.set_title('Conductance distribution (inhibitory)')

			ax_cond.plot(times[mask], state[rf][mask]/1000.)
			ax_cond.set_xlabel('time (ms)')
			ax_cond.set_ylabel('Conductance (\u03bcS)')

			ax_hist.set_ylim((0, 2800))
			ax_hist.hist(state[rf][:19000]/1000., bins=100, range=(0, 0.1))
			ax_hist.set_xlabel('Conductance (\u03bcS)')

	plt.savefig('figure2AB_destexhe2001.pdf')


if __name__ == '__main__':
	state, neuron = simulate_OU_noise_neuron(resolution=1.)
	calc_statistics(state, neuron)
	if TEST_PLOTS:
		plot_results(state)

