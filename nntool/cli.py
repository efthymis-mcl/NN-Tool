"""
nntool

Usage:
    nntool create_project <name>
    nntool train --topology <name> --dataset <name> --epoches <number> --batchsize <number> [--regularization]
    nntool -h | --help
    nntool --version

Options:
    -h --help       Show this screen
    --version       Show version

Examples:
    nntool create_project project1
    nntool train --topology top.txt --dataset iris --epoches 200 --batchsize 120 --regularization
"""


from inspect import getmembers, isclass
from docopt import docopt
from nntool.Trainer import Trainer
from nntool.datasets import *
import os


from . import __version__ as VERSION

def main():
    """Main CLI entrypoint."""
    options = docopt(__doc__, version=VERSION)
    if options['create_project'] is True and options['<name>'] is not None:
        pr_name = options['<name>'][0]
        os.makedirs(pr_name+'/weights')
        os.makedirs(pr_name+'/scripts')
        os.makedirs(pr_name+'/csvresults')
        os.makedirs(pr_name+'/.DATASETS')
    elif options['train'] and options['--topology'] and options['--dataset'] and options['<name>'] is not None:
        trainer = Trainer(options['<name>'][0])
        data_name=options['<name>'][1]
        dsets = datasets()
        if data_name=='iris':
            Train_Examples, Train_Labels, Test_Examples, Test_Labels, Set_Names = dsets.iris()
        elif data_name=='mnist':
            Train_Examples, Train_Labels, Test_Examples, Test_Labels, Set_Names = dsets.mnist()
        elif data_name=='cfar10':
            Train_Examples, Train_Labels, Test_Examples, Test_Labels, Set_Names = dsets.cifar10()
        elif data_name=='chars74k':
            Train_Examples, Train_Labels, Test_Examples, Test_Labels, Set_Names = dsets.chars74k_num_caps_fonts()
        elif data_name=='fashion_mnist':
            Train_Examples, Train_Labels, Test_Examples, Test_Labels, Set_Names = dsets.fashion_mnist()
        else:
            assert 1==0, 'not find dataset'
        trainer.SetData(Train_Examples, Train_Labels, Test_Examples, Test_Labels, Set_Names)
        trainer.SetSession()
        N_Epoch = int(options['<number>'][0])
        BatchSize = int(options['<number>'][1])
        regularization=bool(options['--regularization'])
        trainer.TRAIN(N_Epoch, BatchSize, Tb=3, Te=1, test_predict=True,regularization=regularization)
        trainer.save_weights()