wb_cond_exp
###########

Name: wb_cond_exp - Wang buzsaki model

Description:

wb_cond_exp is an implementation of a modified Hodkin-Huxley model
(1) Post-synaptic currents
 Incoming spike events induce a post-synaptic change of conductance modeled
 by an exponential function.

(2) Spike Detection
 Spike detection is done by a combined threshold-and-local-maximum search: if
 there is a local maximum above a certain threshold of the membrane potential,
 it is considered a spike.

References:

Wang, X.J. and Buzsaki, G., (1996) Gamma oscillation by synaptic inhibition in a hippocampal interneuronal network model. Journal of neuroscience, 16(20), pp.6402-6413.


SeeAlso: hh_cond_exp_traub


Parameters
++++++++++



.. csv-table::
    :header: "Name", "Physical unit", "Default value", "Description"
    :widths: auto

    
    "t_ref", "ms", "2.0ms", "Refractory period"    
    "g_Na", "nS", "3500.0nS", "Sodium peak conductance"    
    "g_K", "nS", "900.0nS", "Potassium peak conductance"    
    "g_L", "nS", "10nS", "Leak conductance"    
    "C_m", "pF", "100.0pF", "Membrane Capacitance"    
    "E_Na", "mV", "55.0mV", "Sodium reversal potential"    
    "E_K", "mV", "-90.0mV", "Potassium reversal potentia"    
    "E_L", "mV", "-65.0mV", "Leak reversal Potential (aka resting potential)"    
    "V_Tr", "mV", "-55.0mV", "Spike Threshold"    
    "tau_syn_ex", "ms", "0.2ms", "Rise time of the excitatory synaptic alpha function i"    
    "tau_syn_in", "ms", "10.0ms", "Rise time of the inhibitory synaptic alpha function"    
    "E_ex", "mV", "0.0mV", "Excitatory synaptic reversal potential"    
    "E_in", "mV", "-75.0mV", "Inhibitory synaptic reversal potential"    
    "I_e", "pA", "0pA", "constant external input current"




State variables
+++++++++++++++

.. csv-table::
    :header: "Name", "Physical unit", "Default value", "Description"
    :widths: auto

    
    "V_m", "mV", "-65.0mV", "Membrane potential"    
    "alpha_n_init", "1 / ms", "-0.05 / (ms * mV) * (V_m + 34.0mV) / (exp(-0.1 * (V_m + 34.0mV)) - 1.0)", ""    
    "beta_n_init", "1 / ms", "0.625 / ms * exp(-(V_m + 44.0mV) / 80.0mV)", ""    
    "alpha_m_init", "1 / ms", "0.1 / (ms * mV) * (V_m + 35.0mV) / (1.0 - exp(-0.1mV * (V_m + 35.0mV)))", ""    
    "beta_m_init", "1 / ms", "4.0 / (ms) * exp(-(V_m + 60.0mV) / 18.0mV)", ""    
    "alpha_h_init", "1 / ms", "0.35 / ms * exp(-(V_m + 58.0mV) / 20.0mV)", ""    
    "beta_h_init", "1 / ms", "5.0 / (exp(-0.1 / mV * (V_m + 28.0mV)) + 1.0) / ms", ""    
    "Inact_h", "real", "alpha_h_init / (alpha_h_init + beta_h_init)", "Act_m real = alpha_m_init / ( alpha_m_init + beta_m_init )"    
    "Act_n", "real", "alpha_n_init / (alpha_n_init + beta_n_init)", ""




Equations
+++++++++




.. math::
   \frac{ dV_{m} } { dt }= \frac 1 { C_{m} } \left( { (-(I_{Na} + I_{K} + I_{L}) + I_{e} + I_{stim} + I_{syn,inh} + I_{syn,exc}) } \right) 


.. math::
   \frac{ dAct_{n} } { dt }= (\alpha_{n} \cdot (1 - Act_{n}) - \beta_{n} \cdot Act_{n})


.. math::
   \frac{ dInact_{h} } { dt }= (\alpha_{h} \cdot (1 - Inact_{h}) - \beta_{h} \cdot Inact_{h})





Source code
+++++++++++

.. code:: nestml

    neuron wb_cond_exp:
      state:
        r integer = 0 # number of steps in the current refractory phase

        V_m mV = E_L    # Membrane potential

        Inact_h real = alpha_h_init / ( alpha_h_init + beta_h_init )
        Act_n real = alpha_n_init / ( alpha_n_init + beta_n_init )
      end

      equations:
        # synapses: exponential conductance
        kernel g_in = exp(-1.0 / tau_syn_in * t)
        kernel g_ex = exp(-1.0 / tau_syn_ex * t)

        recordable inline I_syn_exc pA = convolve(g_ex, spikeExc) * ( V_m - E_ex )
        recordable inline I_syn_inh pA = convolve(g_in, spikeInh) * ( V_m - E_in )

        inline I_Na  pA = g_Na * _subexpr(V_m) * Inact_h * ( V_m - E_Na )
        inline I_K   pA  = g_K * Act_n**4 * ( V_m - E_K )
        inline I_L   pA = g_L * ( V_m - E_L )

        V_m' =( -( I_Na + I_K + I_L ) + I_e + I_stim + I_syn_inh + I_syn_exc ) / C_m
        Act_n' = ( alpha_n(V_m) * ( 1 - Act_n ) - beta_n(V_m) * Act_n )  # n-variable
        Inact_h' = ( alpha_h(V_m) * ( 1 - Inact_h ) - beta_h(V_m) * Inact_h ) # h-variable
      end

      parameters:
        t_ref ms = 2.0 ms           # Refractory period
        g_Na nS = 3500.0 nS         # Sodium peak conductance
        g_K nS = 900.0 nS           # Potassium peak conductance
        g_L nS = 10 nS              # Leak conductance
        C_m pF = 100.0 pF           # Membrane Capacitance
        E_Na mV = 55.0 mV           # Sodium reversal potential
        E_K mV = -90.0 mV           # Potassium reversal potentia
        E_L mV = -65.0 mV           # Leak reversal Potential (aka resting potential)
        V_Tr mV = -55.0 mV          # Spike Threshold
        tau_syn_ex ms = 0.2 ms      # Rise time of the excitatory synaptic alpha function i
        tau_syn_in ms = 10.0 ms     # Rise time of the inhibitory synaptic alpha function
        E_ex mV = 0.0 mV            # Excitatory synaptic reversal potential
        E_in mV = -75.0 mV          # Inhibitory synaptic reversal potential

        # constant external input current
        I_e pA = 0 pA
      end

      internals:
        RefractoryCounts integer = steps(t_ref) # refractory time in steps

        alpha_n_init 1/ms = -0.05/(ms*mV) * (E_L + 34.0 mV) / (exp(-0.1 * (E_L + 34.0 mV)) - 1.0)
        beta_n_init  1/ms = 0.625/ms * exp(-(E_L + 44.0 mV) / 80.0 mV)
        alpha_h_init 1/ms = 0.35/ms * exp(-(E_L + 58.0 mV) / 20.0 mV)
        beta_h_init  1/ms = 5.0 / (exp(-0.1 / mV * (E_L + 28.0 mV)) + 1.0) /ms
      end

      input:
        spikeInh nS <- inhibitory spike
        spikeExc nS <- excitatory spike
        I_stim pA <- continuous
      end

      output: spike

      update:
        U_old mV = V_m
        integrate_odes()
        # sending spikes: crossing 0 mV, pseudo-refractoriness and local maximum...
        if r > 0: # is refractory?
          r -= 1
        elif V_m > V_Tr and U_old > V_m: # threshold && maximum
          r = RefractoryCounts
          emit_spike()
        end
      end

      function _subexpr(V_m mV) real:
        return alpha_m(V_m)**3 / ( alpha_m(V_m) + beta_m(V_m) )**3
      end

      function alpha_m(V_m mV) 1/ms:
        return 0.1/(ms*mV) * (V_m + 35.0 mV) / (1.0 - exp(-0.1 mV * (V_m + 35.0 mV)))
      end

      function beta_m(V_m mV) 1/ms:
        return 4.0/(ms) * exp(-(V_m + 60.0 mV) / 18.0 mV)
      end

      function alpha_n(V_m mV) 1/ms:
        return -0.05/(ms*mV) * (V_m + 34.0 mV) / (exp(-0.1 * (V_m + 34.0 mV)) - 1.0)
      end

      function beta_n(V_m mV) 1/ms:
        return 0.625/ms * exp(-(V_m + 44.0 mV) / 80.0 mV)
      end

      function alpha_h(V_m mV) 1/ms:
        return 0.35/ms * exp(-(V_m + 58.0 mV) / 20.0 mV)
      end

      function beta_h(V_m mV) 1/ms:
        return 5.0 / (exp(-0.1 / mV * (V_m + 28.0 mV)) + 1.0) /ms
      end

    end




Characterisation
++++++++++++++++

.. include:: wb_cond_exp_characterisation.rst


.. footer::

   Generated at 2020-05-27 18:26:44.707062