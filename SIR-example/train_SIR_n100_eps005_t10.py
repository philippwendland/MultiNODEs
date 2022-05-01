import numpy as np
import torch
import pandas as pd
import processing as pr

import main as m

if __name__ == "__main__":

    adjoint = True #using of adjoint method
    train_dir = '../../train'
    
    # check, whether cuda is available or not
    gpu = 0
    device = torch.device('cuda:' + str(gpu)
                          if torch.cuda.is_available() else 'cpu')
    
    # initiate model
    
    mypath = '/home/bio/groupshare/pwendland/masterarbeit-philipp/NeuralODE_code/Analyse/SIR'
    #mypath = r'C:\Users\User\Documents\GitHub\masterarbeit-philipp\NeuralODE_code\Analyse\SIR'
    mypath = '/home/pwendland/Dokumente/GitHub/mnode/NeuralODE_code/SIR/SIR_synth_new2'
    train_dir = mypath
    #------ Raw Data -------
    
    varSIR = pd.read_csv(mypath + '/SIR_n100_eps005.csv',
                       sep=',',header=0, 
                       index_col=0, engine='python')
    
    n = len(varSIR) #number of persons
    #timesteps equal to months
    timesteps = np.linspace(0, 40, 200)
    
    tover = timesteps/200 #relative values of time
    temps = len(timesteps)
    var = 3
    
    values = varSIR.values
    varnames = varSIR.columns
    IDs = varSIR.index
    
    dataset = np.reshape(values, (n, var, temps))
    dataset = np.swapaxes(dataset, 1, 2)
    #dataset has 3 indices, first one is person, second one is visits, third one is variable
    
    X_train, W_train = pr.weighter(dataset)
    #zeros are the missing values, W_train describes, whether a value is missing or not
    
    #logFolder = '/Performance/logs/TimeDependent/DataPred/ODENN/bmode_data/'
    
    beta=0.2
    gamma=1/10
    static = np.empty((20,2))
    static[:] = np.array((beta,gamma))
    
    static = torch.from_numpy(static)
    
    static_types=np.array([['real',1],['real',1]],dtype=np.object)
    
    static_missing = None
    
    staticdata_onehot, staticdata_types_dict, static_miss_mask, static_true_miss_mask, static_n_samples = m.read_data(static,static_types,static_missing)
    
    samp_trajs = X_train
    
    index = np.linspace(0,199,10,dtype=int)
    samp_trajs = samp_trajs[80:100,tuple(index),:]
    
    W_train = W_train[80:100,tuple(index),:]
    
    samp_trajs = torch.from_numpy(samp_trajs).float().to(device)
    samp_ts = torch.from_numpy(index/199*40).float().to(device)
    
    samp_trajs=samp_trajs/1000
    
    obs_dim = var
    
    batch_norm_static = False
    dectype='orig'
    adjoint=True
    
    #FrozenTrial(number=46, values=[0.001628006575629115]
    lr = 0.00601775920584171
    latent_dim = 1.010561217834188
    nhidden = 3.6777847577609126
    batchsize = 0.3567612219833565
    activation_ode = 'none'
    num_odelayers = 4
    enctype = 'RNN'
    activation_rnn = 'relu'
    activation_dec = 'relu'
    dropout_dec = 0.048294395239418614
    rnn_nhidden_enc = 0.7504019762037379
    rnn_nhidden_dec = 0.9328043779498616
    s_dim_static = 1
    z_dim_static = 6
    scaling_ELBO = 0.6323358754903038
    nepochs=579
    
    batch_norm_static = False
    dectype='orig'
    solver = '/home/pwendland/Downloads/torch_ACA-dense_state2/'
    #activation_rnn=None
    
    nepochs=1
    
    loss, rec_loss, kl= m.training(solver, nepochs, lr, train_dir, device, samp_trajs, samp_ts, latent_dim, nhidden, obs_dim, batchsize, activation_ode = activation_ode,num_odelayers = num_odelayers, W_train = W_train, enctype = enctype,dectype = dectype, rnn_nhidden_enc=rnn_nhidden_enc,activation_rnn = activation_rnn,rnn_nhidden_dec=rnn_nhidden_dec,activation_dec = activation_dec,dropout_dec = dropout_dec,static=static,staticdata_onehot=staticdata_onehot,staticdata_types_dict=staticdata_types_dict,static_true_miss_mask=static_true_miss_mask,s_dim_static=s_dim_static,z_dim_static=z_dim_static,scaling_ELBO=scaling_ELBO,batch_norm_static=batch_norm_static)
    
    #limits of simulated time
    timemax = 40
    timemin = 0
    
    negtime= False
    
    sigmalong=1
    sigmastat=1
    N=1
    
    xs_pos_rec, ts_pos, out_rec, qz0_mean_rec, qz0_sigma_rec, epsilon_rec, qz0_meanstat_rec, qz0sigma_rec,epsilonstat_rec = m.reconRP(solver, train_dir, device,samp_trajs,samp_ts, latent_dim, nhidden, obs_dim, activation_ode = activation_ode,num_odelayers=num_odelayers,W_train=W_train, enctype = enctype,dectype = dectype, rnn_nhidden_enc=rnn_nhidden_enc,activation_rnn = activation_rnn,rnn_nhidden_dec=rnn_nhidden_dec,activation_dec = activation_dec,static=static,staticdata_onehot=staticdata_onehot,staticdata_types_dict=staticdata_types_dict,static_true_miss_mask=static_true_miss_mask,s_dim_static=s_dim_static,z_dim_static=z_dim_static,batch_norm_static=batch_norm_static, timemax = timemax, negtime = False, timemin = None,num=2000)
    
    #xs_pos_rec, out_rec, qz0_mean_rec, qz0_sigma_rec, epsilon_rec, qz0_meanstat_rec, qz0sigma_rec,epsilonstat_rec = m.valloss(adjoint, train_dir, device,samp_trajs,samp_ts, latent_dim, nhidden, obs_dim, activation_ode = activation_ode,num_odelayers=num_odelayers,W_train=W_train, enctype = enctype,dectype = dectype, rnn_nhidden_enc=rnn_nhidden_enc,activation_rnn = activation_rnn,rnn_nhidden_dec=rnn_nhidden_dec,activation_dec = activation_dec,static=static,staticdata_onehot=staticdata_onehot,staticdata_types_dict=staticdata_types_dict,static_true_miss_mask=static_true_miss_mask,s_dim_static=s_dim_static,z_dim_static=z_dim_static,batch_norm_static=batch_norm_static)
    
    xs_pos_posterior, ts_pos_posterior, out_posterior, qz0_mean_posterior, logsigma_posterior, epsilon_posterior, qz0_meanstat_posterior, logsigmastat_posterior,epsilonstat_posterior = m.generationPosterior(solver, train_dir, device,samp_trajs,samp_ts, latent_dim, nhidden, obs_dim, activation_ode = activation_ode,num_odelayers=num_odelayers,W_train=W_train, enctype = enctype,dectype = dectype, rnn_nhidden_enc=rnn_nhidden_enc,activation_rnn = activation_rnn,rnn_nhidden_dec=rnn_nhidden_dec,activation_dec = activation_dec,static=static,staticdata_onehot=staticdata_onehot,staticdata_types_dict=staticdata_types_dict,static_true_miss_mask=static_true_miss_mask,s_dim_static=s_dim_static,z_dim_static=z_dim_static,batch_norm_static=batch_norm_static, timemax = timemax, negtime = False, timemin = None,num=2000, sigmalong=sigmalong,sigmastat=sigmastat,N=N)
    
    varnamessave = ["MedicalHistory_WGTKG","MedicalHistory_HTCM","MedicalHistory_TEMPC","MedicalHistory_SYSSUP","MedicalHistory_DIASUP","MedicalHistory_HRSUP","MedicalHistory_SYSSTND","MedicalHistory_DIASTND","MedicalHistory_HRSTND","NonMotor_DVT_TOTAL_RECALL","NonMotor_DVS_LNS","NonMotor_BJLOT","NonMotor_ESS","NonMotor_GDS","NonMotor_QUIP","NonMotor_RBD","NonMotor_SCOPA","NonMotor_SFT","NonMotor_STA","NonMotor_STAI.State","NonMotor_STAI.Trait","UPDRS_UPDRS1","UPDRS_UPDRS2","UPDRS_UPDRS3","SA_CSF_CSF.Alpha.synuclein"]
    varnamesstatic = ["CSF_Abeta.42_VIS00","CSF_p.Tau181P_VIS00","CSF_Total.tau_VIS00","CSF_tTau.Abeta_VIS00","CSF_pTau.Abeta_VIS00","CSF_pTau.tTau_VIS00","Biological_ALDH1A1..rep.1._VIS00","Biological_ALDH1A1..rep.2._VIS00","Biological_GAPDH..rep.1._VIS00","Biological_GAPDH..rep.2._VIS00","Biological_HSPA8..rep.1._VIS00","Biological_HSPA8..rep.2._VIS00","Biological_LAMB2..rep.1._VIS00","Biological_LAMB2..rep.2._VIS00","Biological_PGK1..rep.1._VIS00","Biological_PGK1..rep.2._VIS00","Biological_PSMC4..rep.1._VIS00","Biological_PSMC4..rep.2._VIS00","Biological_SKP1..rep.1._VIS00","Biological_SKP1..rep.2._VIS00","Biological_UBE2K..rep.1._VIS00","Biological_UBE2K..rep.2._VIS00","Biological_Serum.IGF.1_VIS00","PatDemo_HISPLAT","PatDemo_RAINDALS","PatDemo_RAASIAN","PatDemo_RABLACK","PatDemo_RAWHITE","PatDemo_RANOS","PatDemo_EDUCYRS","PatDemo_HANDED","PatDemo_GENDER","PatPDHist_BIOMOMPD","PatPDHist_BIODADPD","PatPDHist_FULSIBPD","PatPDHist_MAGPARPD","PatPDHist_PAGPARPD","PatPDHist_MATAUPD","PatPDHist_PATAUPD","SA_Imaging_VIS00","SA_Enrollment_Age","SA_CADD_filtered_impact_scores_VIS00","SA_Polygenetic_risk_scores_VIS00"]
    
    varnamessave = ["Suscepible","Infected","Removed"]
    varnamesstatic = ["Beta","Gamma"]
    
    torch.save({'Recon_values': xs_pos_rec,
                'Recon_time': ts_pos,
                'varnames': varnamessave,
                'orig_time': samp_ts,
                'static_values': out_rec,
                'varnamesstatic':varnamesstatic,
                'W_train': W_train}
                ,train_dir + '/Reconstruction_n2100_eps005_t10_normed.pth')
    
    torch.save({'Generation_values': xs_pos_posterior,
                'Generation_time':ts_pos_posterior,
                'varnames': varnamessave,
                'orig_time': samp_ts,
                'static_values': out_posterior,
                'varnamesstatic':varnamesstatic}
                ,train_dir + '/Generationposterior_n2100_eps005_t10_normed.pth')
    
    
    
        
