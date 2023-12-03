import matplotlib.pyplot as plt

def combinedplot(bandfile, dosfile):
    
    fig, axs = plt.subplots(1, 2, gridspec_kw={'width_ratios': [4, 1]},  figsize = (20, 15))
    with open(bandfile, 'r') as f:
        funcx = f.read()
        lines = funcx.split('\n')
    
    endpattern = '# EFERMI (HARTREE)'
    startpattern1 = '@ VIEW      0.15000,     0.15000,     0.63709,     0.85000'
    startpattern2 = '@ VIEW      0.65709,     0.15000,     1.14418,     0.85000'
    xtickpattern = 'XAXIS TICK    '

    xticks = []
    eindices = []
    s1index = 0
    s2index = 0
    
    for i, line in enumerate(lines):
        if endpattern in line:
            eindices.append(i)
        if startpattern1 in line:
            s1index += (i)
        if startpattern2 in line:
            s2index += (i)
        if xtickpattern in line:
            xticks.append(i)
    
    xticks = xticks[1:4]
    M = float(lines[xticks[0]].strip().split()[4])
    K = float(lines[xticks[1]].strip().split()[4])
    G = float(lines[xticks[2]].strip().split()[4])
    tickpositions = [0, M, K, G]
    ticklabel = ['\u0393', 'M', 'K', '\u0393']
    alpha = lines[s1index+1:int(eindices[0])]
    beta = lines[s2index+1:int(eindices[1])]
    efermi = lines[int(eindices[1])].strip().split()
    print('Fermi energy in Ha Au ' + efermi[3])

    alpha_list = [list() for n in range(len(alpha[0].strip().split()))]
    beta_list = [list() for n in range(len(beta[0].strip().split()))]
    for i in alpha:
        splitval = i.strip().split()
        for n in range(len(splitval)):
            alpha_list[n].append(float(splitval[n]))
    for i in beta:
        splitval = i.strip().split()
        for n in range(len(splitval)):
            beta_list[n].append(float(splitval[n]))   
    
    
    with open(dosfile, 'r') as dos:
        dosx = dos.read()
        dos_lines = dosx.split('\n')
    
    enddos = '# EFERMI (HARTREE)'
    startdos1 = '@ YAXIS LABEL "DENSITY OF STATES (STATES/HARTREE/CELL)'
    startdos2 = '&'

    edos = []
    s1dos = 0
    s2dos = 0
    
    for n, l in enumerate(dos_lines):
        if enddos in l:
            edos.append(n)
        if startdos1 in l:
            s1dos += (n)
        if startdos2 in l:
            s2dos += (n)

    alpha_dos = dos_lines[s1dos+1:int(edos[0])]
    beta_dos = dos_lines[s2dos+1:int(edos[1])]
    
    xalpha,yalpha = [], []
    for i in alpha_dos:
        splitvald = i.strip().split()
        for n in range(len(splitvald)):
            xalpha.append(float(splitvald[0]))
            yalpha.append(float(splitvald[1]))
    
    xbeta,ybeta = [], []
    for i in beta_dos:
        splitvald = i.strip().split()
        for n in range(len(splitvald)):
            xbeta.append(float(splitvald[0]))
            ybeta.append(float(splitvald[1]))
                                
    yminval = min(xalpha)
    ymaxval = max(xalpha)
    xmaxval = max(alpha_list[0])
                                
                                
    for m in range(1,len(splitval)):
        axs[0].plot(alpha_list[0], alpha_list[m], color = 'mediumblue', label = 'Alpha')
        axs[0].plot(beta_list[0], beta_list[m], color = 'red', label = 'Beta')
        axs[0].vlines(x = 0, ymin = yminval, ymax = ymaxval, color = 'k')
        axs[0].vlines(x = M, ymin = yminval, ymax = ymaxval, color = 'k')
        axs[0].vlines(x = K, ymin = yminval, ymax = ymaxval, color = 'k')
        axs[0].vlines(x = G, ymin = yminval, ymax = ymaxval, color = 'k')
        axs[0].hlines(y=0, xmin=0, xmax= xmaxval, color='k', linestyle = '--')
        axs[0].set_xticks(tickpositions)
        axs[0].set_xticklabels(ticklabel)
        axs[0].set_ylabel('\u0394E = E - $E_{F}$ Ha AU')
        axs[0].set_title('BAND')
                                
    axs[1].plot(yalpha, xalpha, color = 'mediumblue', label = 'Alpha')
    axs[1].plot(ybeta, xbeta, color = 'red', label = 'Beta')
    axs[1].get_yaxis().set_ticks([])
    axs[1].vlines(x = 0, ymin = yminval, ymax = ymaxval, color = 'k', linestyle = '--')
    axs[1].set_title('DOS')
    
    return 