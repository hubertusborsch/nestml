wb_cond_multisyn
################

Name: wb_cond_multisyn - Wang buzsaki model with 

Description:

wb_cond_multisyn is an implementation of a modified Hodkin-Huxley model

Spike Detection
 Spike detection is done by a combined threshold-and-local-maximum search: if
 there is a local maximum above a certain threshold of the membrane potential,
 it is considered a spike.

- AMPA, NMDA, GABA_A, and GABA_B conductance-based synapses with
 beta-function (difference of two exponentials) time course.

References:

Wang, X.J. and Buzsaki, G., (1996) Gamma oscillation by synaptic inhibition in a hippocampal interneuronal network model. Journal of neuroscience, 16(20), pp.6402-6413.

SeeAlso: hill_tononi


Parameters
++++++++++



.. csv-table::
    :header: "Name", "Physical unit", "Default value", "Description"
    :widths: auto

    
    "t_ref", "ms", "2.0ms", "Refractory period 2.0"    
    "g_Na", "nS", "3500.0nS", "Sodium peak conductance"    
    "g_K", "nS", "900.0nS", "Potassium peak conductance"    
    "g_L", "nS", "10nS", "Leak conductance"    
    "C_m", "pF", "100.0pF", "Membrane Capacitance"    
    "E_Na", "mV", "55.0mV", "Sodium reversal potential"    
    "E_K", "mV", "-90.0mV", "Potassium reversal potentia"    
    "E_L", "mV", "-65.0mV", "Leak reversal Potential (aka resting potential)"    
    "V_Tr", "mV", "-55.0mV", "Spike Threshold"    
    "AMPA_g_peak", "nS", "0.1nS", "Parameters for synapse of type AMPA, GABA_A, GABA_B and NMDApeak conductance"    
    "AMPA_E_rev", "mV", "0.0mV", "reversal potential"    
    "AMPA_Tau_1", "ms", "0.5ms", "rise time"    
    "AMPA_Tau_2", "ms", "2.4ms", "decay time, Tau_1 < Tau_2"    
    "NMDA_g_peak", "nS", "0.075nS", "peak conductance"    
    "NMDA_Tau_1", "ms", "4.0ms", "rise time"    
    "NMDA_Tau_2", "ms", "40.0ms", "decay time, Tau_1 < Tau_2"    
    "NMDA_E_rev", "mV", "0.0mV", "reversal potential"    
    "NMDA_Vact", "mV", "-58.0mV", "inactive for V << Vact, inflection of sigmoid"    
    "NMDA_Sact", "mV", "2.5mV", "scale of inactivation"    
    "GABA_A_g_peak", "nS", "0.33nS", "peak conductance"    
    "GABA_A_Tau_1", "ms", "1.0ms", "rise time"    
    "GABA_A_Tau_2", "ms", "7.0ms", "decay time, Tau_1 < Tau_2"    
    "GABA_A_E_rev", "mV", "-70.0mV", "reversal potential"    
    "GABA_B_g_peak", "nS", "0.0132nS", "peak conductance"    
    "GABA_B_Tau_1", "ms", "60.0ms", "rise time"    
    "GABA_B_Tau_2", "ms", "200.0ms", "decay time, Tau_1 < Tau_2"    
    "GABA_B_E_rev", "mV", "-90.0mV", "reversal potential for intrinsic current"    
    "I_e", "pA", "0pA", "constant external input current"




State variables
+++++++++++++++

.. csv-table::
    :header: "Name", "Physical unit", "Default value", "Description"
    :widths: auto

    
    "V_m", "mV", "-65.0mV", "Membrane potential"    
    "alpha_n_init", "real", "-0.05 * (V_m / mV + 34.0) / (exp(-0.1 * (V_m / mV + 34.0)) - 1.0)", "function alpha_n_init real = 0.032 * (V_m / mV + 52.) / (1. - exp(-(V_m / mV + 52.) / 5.))"    
    "beta_n_init", "real", "0.625 * exp(-(V_m / mV + 44.0) / 80.0)", ""    
    "alpha_m_init", "real", "0.1 * (V_m / mV + 35.0) / (1.0 - exp(-0.1mV * (V_m / mV + 35.0mV)))", ""    
    "beta_m_init", "real", "4.0 * exp(-(V_m / mV + 60.0) / 18.0)", ""    
    "alpha_h_init", "real", "0.35 * exp(-(V_m / mV + 58.0) / 20.0)", ""    
    "beta_h_init", "real", "5.0 / (exp(-0.1 * (V_m / mV + 28.0)) + 1.0)", ""    
    "Inact_h", "real", "alpha_h_init / (alpha_h_init + beta_h_init)", "Act_m real =  alpha_m_init / ( alpha_m_init + beta_m_init )    Activation variable m for NaInactivation variable h for Na"    
    "Act_n", "real", "alpha_n_init / (alpha_n_init + beta_n_init)", "Activation variable n for K"    
    "g_AMPA", "nS", "0.0nS", ""    
    "g_AMPA__d", "nS / ms", "0.0nS / ms", ""    
    "g_NMDA", "nS", "0.0nS", ""    
    "g_NMDA__d", "nS / ms", "0.0nS / ms", ""    
    "g_GABAA", "nS", "0.0nS", ""    
    "g_GABAA__d", "nS / ms", "0.0nS / ms", ""    
    "g_GABAB", "nS", "0.0nS", ""    
    "g_GABAB__d", "nS / ms", "0.0nS / ms", ""




Equations
+++++++++




.. math::
   \frac{ dInact_{h} } { dt }= \frac 1 { \mathrm{ms} } \left( { (\alpha_{h} \cdot (1 - Inact_{h}) - \beta_{h} \cdot Inact_{h}) } \right) 


.. math::
   \frac{ dAct_{n} } { dt }= \frac 1 { \mathrm{ms} } \left( { (\alpha_{n} \cdot (1 - Act_{n}) - \beta_{n} \cdot Act_{n}) } \right) 


.. math::
   \frac{ dV_{m} } { dt }= \frac 1 { C_{m} } \left( { (-(I_{Na} + I_{K} + I_{L}) + I_{e} + I_{stim} + I_{syn}) } \right) 


.. math::
   \frac{ dg_{AMPA,,d} } { dt }= \frac{ -g_{AMPA,,d} } { AMPA_{\Tau,1} }


.. math::
   \frac{ dg_{AMPA} } { dt }= g_{AMPA,,d} - \frac{ g_{AMPA} } { AMPA_{\Tau,2} }


.. math::
   \frac{ dg_{NMDA,,d} } { dt }= \frac{ -g_{NMDA,,d} } { NMDA_{\Tau,1} }


.. math::
   \frac{ dg_{NMDA} } { dt }= g_{NMDA,,d} - \frac{ g_{NMDA} } { NMDA_{\Tau,2} }


.. math::
   \frac{ dg_{GABAA,,d} } { dt }= \frac{ -g_{GABAA,,d} } { GABA_{A,\Tau,1} }


.. math::
   \frac{ dg_{GABAA} } { dt }= g_{GABAA,,d} - \frac{ g_{GABAA} } { GABA_{A,\Tau,2} }


.. math::
   \frac{ dg_{GABAB,,d} } { dt }= \frac{ -g_{GABAB,,d} } { GABA_{B,\Tau,1} }


.. math::
   \frac{ dg_{GABAB} } { dt }= g_{GABAB,,d} - \frac{ g_{GABAB} } { GABA_{B,\Tau,2} }





Source code
+++++++++++

.. code:: nestml

    neuron wb_cond_multisyn:
      state:
        r integer = 0 # number of steps in the current refractory phase

        V_m mV = -65. mV # Membrane potential
        Inact_h real = alpha_h_init / ( alpha_h_init + beta_h_init )    # Inactivation variable h for Na
        Act_n real = alpha_n_init / (alpha_n_init + beta_n_init)  # Activation variable n for K

        g_AMPA real = 0
        g_NMDA real = 0
        g_GABAA real = 0
        g_GABAB real = 0
        g_AMPA$ real = AMPAInitialValue
        g_NMDA$ real = NMDAInitialValue
        g_GABAA$ real = GABA_AInitialValue
        g_GABAB$ real = GABA_BInitialValue
      end

      equations:
        recordable inline I_syn_ampa pA = -convolve(g_AMPA, AMPA) * ( V_m - AMPA_E_rev )
        recordable inline I_syn_nmda pA = -convolve(g_NMDA, NMDA) * ( V_m - NMDA_E_rev ) / ( 1 + exp( ( NMDA_Vact - V_m ) / NMDA_Sact ) )
        recordable inline I_syn_gaba_a pA = -convolve(g_GABAA, GABA_A) * ( V_m - GABA_A_E_rev )
        recordable inline I_syn_gaba_b pA = -convolve(g_GABAB, GABA_B) * ( V_m - GABA_B_E_rev )
        recordable inline I_syn pA = I_syn_ampa + I_syn_nmda + I_syn_gaba_a + I_syn_gaba_b

        inline I_Na  pA = g_Na * Act_m_inf(V_m)**3 * Inact_h * ( V_m - E_Na )
        inline I_K   pA = g_K * Act_n**4 * ( V_m - E_K )
        inline I_L   pA = g_L * ( V_m - E_L )

        Inact_h' = ( alpha_h(V_m) * ( 1 - Inact_h ) - beta_h(V_m) * Inact_h ) / ms # h-variable
        Act_n' = ( alpha_n(V_m) * ( 1 - Act_n ) - beta_n(V_m) * Act_n ) / ms # n-variable
        V_m' = ( -( I_Na + I_K + I_L ) + I_e + I_stim + I_syn ) / C_m


        #############
        # Synapses
        #############

        kernel g_AMPA' = g_AMPA$ - g_AMPA / AMPA_Tau_2,
               g_AMPA$' = -g_AMPA$ / AMPA_Tau_1

        kernel g_NMDA' = g_NMDA$ - g_NMDA / NMDA_Tau_2,
               g_NMDA$' = -g_NMDA$ / NMDA_Tau_1

        kernel g_GABAA' = g_GABAA$ - g_GABAA / GABA_A_Tau_2,
               g_GABAA$' = -g_GABAA$ / GABA_A_Tau_1

        kernel g_GABAB' = g_GABAB$ - g_GABAB / GABA_B_Tau_2,
               g_GABAB$' = -g_GABAB$ / GABA_B_Tau_1
      end

      parameters:
        t_ref ms = 2.0 ms      # Refractory period 2.0
        g_Na nS = 3500.0 nS    # Sodium peak conductance
        g_K nS = 900.0 nS      # Potassium peak conductance
        g_L nS = 10 nS          # Leak conductance
        C_m pF = 100.0 pF       # Membrane Capacitance
        E_Na mV = 55.0 mV         # Sodium reversal potential
        E_K mV = -90.0 mV        # Potassium reversal potentia
        E_L mV = -65.0 mV     # Leak reversal Potential (aka resting potential)
        V_Tr mV = -55.0 mV        # Spike Threshold

        # Parameters for synapse of type AMPA, GABA_A, GABA_B and NMDA
        AMPA_g_peak nS = 0.1 nS      # peak conductance
        AMPA_E_rev mV = 0.0 mV       # reversal potential
        AMPA_Tau_1 ms = 0.5 ms       # rise time
        AMPA_Tau_2 ms = 2.4 ms       # decay time, Tau_1 < Tau_2

        NMDA_g_peak nS = 0.075 nS    # peak conductance
        NMDA_Tau_1 ms = 4.0 ms       # rise time
        NMDA_Tau_2 ms = 40.0 ms      # decay time, Tau_1 < Tau_2
        NMDA_E_rev mV = 0.0 mV       # reversal potential
        NMDA_Vact mV = -58.0 mV      # inactive for V << Vact, inflection of sigmoid
        NMDA_Sact mV = 2.5 mV        # scale of inactivation

        GABA_A_g_peak nS = 0.33 nS   # peak conductance
        GABA_A_Tau_1 ms = 1.0 ms     # rise time
        GABA_A_Tau_2 ms = 7.0 ms     # decay time, Tau_1 < Tau_2
        GABA_A_E_rev mV = -70.0 mV   # reversal potential

        GABA_B_g_peak nS = 0.0132 nS # peak conductance
        GABA_B_Tau_1 ms = 60.0 ms    # rise time
        GABA_B_Tau_2 ms = 200.0 ms   # decay time, Tau_1 < Tau_2
        GABA_B_E_rev mV = -90.0 mV   # reversal potential for intrinsic current

        # constant external input current
        I_e pA = 0 pA
      end

      internals:
        AMPAInitialValue real = compute_synapse_constant( AMPA_Tau_1, AMPA_Tau_2, AMPA_g_peak )
        NMDAInitialValue real = compute_synapse_constant( NMDA_Tau_1, NMDA_Tau_2, NMDA_g_peak )
        GABA_AInitialValue real = compute_synapse_constant( GABA_A_Tau_1, GABA_A_Tau_2, GABA_A_g_peak )
        GABA_BInitialValue real = compute_synapse_constant( GABA_B_Tau_1, GABA_B_Tau_2, GABA_B_g_peak )
        RefractoryCounts integer = steps(t_ref) # refractory time in steps

        alpha_n_init real = -0.05 * (V_m / mV + 34.0) / (exp(-0.1 * (V_m / mV + 34.0)) - 1.0)
        beta_n_init  real = 0.625 * exp(-(V_m / mV + 44.0) / 80.0)
        alpha_m_init real = 0.1 * (V_m / mV + 35.0) / (1.0 - exp(-0.1 * (V_m / mV + 35.)))
        beta_m_init  real = 4.0 * exp(-(V_m / mV + 60.0) / 18.0)
        alpha_h_init real = 0.35 * exp(-(V_m / mV + 58.0) / 20.0)
        beta_h_init  real = 5.0 / (exp(-0.1 * (V_m / mV + 28.0)) + 1.0)
      end

      input:
        AMPA nS  <- spike
        NMDA nS  <- spike
        GABA_A nS <- spike
        GABA_B nS <- spike
        I_stim pA <- continuous
      end

      output: spike

      update:
        U_old mV = V_m
        integrate_odes()

        # sending spikes:
        if r > 0: # is refractory?
          r -= 1
        elif V_m > V_Tr and U_old > V_m: # threshold && maximum
          r = RefractoryCounts
          emit_spike()
        end

      end

      function compute_synapse_constant(Tau_1 ms, Tau_2 ms, g_peak nS) real:
        # Factor used to account for the missing 1/((1/Tau_2)-(1/Tau_1)) term
        # in the ht_neuron_dynamics integration of the synapse terms.
        # See: Exact digital simulation of time-invariant linear systems
        # with applications to neuronal modeling, Rotter and Diesmann,
        # section 3.1.2.
        exact_integration_adjustment real = ( ( 1 / Tau_2 ) - ( 1 / Tau_1 ) ) * ms

        t_peak ms = ( Tau_2 * Tau_1 ) * ln( Tau_2 / Tau_1 ) / ( Tau_2 - Tau_1 )
        normalisation_factor real = 1 / ( exp( -t_peak / Tau_1 ) - exp( -t_peak / Tau_2 ) )

        return (g_peak / nS) * normalisation_factor * exact_integration_adjustment
      end

      function Act_m_inf(V_m mV) real:
        return alpha_m(V_m) / ( alpha_m(V_m) + beta_m(V_m) )
      end

      function alpha_m(V_m mV) real:
        return 0.1 * (V_m / mV + 35.0) / (1.0 - exp(-0.1 * (V_m / mV + 35.)))
      end

      function beta_m(V_m mV) real:
        return 4.0 * exp(-(V_m / mV + 60.0) / 18.0)
      end

      function alpha_n(V_m mV) real:
        return -0.05 * (V_m / mV + 34.0) / (exp(-0.1 * (V_m / mV + 34.0)) - 1.0)
      end

      function beta_n(V_m mV) real:
        return 0.625 * exp(-(V_m / mV + 44.0) / 80.0)
      end

      function alpha_h(V_m mV) real:
        return 0.35 * exp(-(V_m / mV + 58.0) / 20.0)
      end

      function beta_h(V_m mV) real:
        return 5.0 / (exp(-0.1 * (V_m / mV + 28.0)) + 1.0)
      end

    end



Characterisation
++++++++++++++++

.. include:: wb_cond_multisyn_characterisation.rst


.. footer::

   Generated at 2020-05-27 18:26:44.376228