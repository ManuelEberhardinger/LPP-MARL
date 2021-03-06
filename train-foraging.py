import numpy as np
import pandas as pd
from expert_demonstrations import get_demo, run_foraging_policy
import pickle
import pipeline
import argparse
import os
from lbforaging.agents.expert_policy import expert_policy as expert_foraging_policy

parser = argparse.ArgumentParser(description='Train the logical program policies on the ForagingEnv')
parser.add_argument('--n_demos', type=int, default=10,
                    help='an integer for the accumulator')
parser.add_argument('--num_programs', type=int, default=10000,
                    help='the number of feature detector programs')
parser.add_argument('--num_dt', type=int, default=5,
                    help='the number of decision trees')
parser.add_argument('--max_num_particles', type=int, default=25,
                    help='the max number of particles for the plp')
parser.add_argument('--gen_prog_step_size', type=int, default=1,
                    help='the step size of the program generation loop')
parser.add_argument('--env_name', type=str, default="Foraging-grid-6x6-2p-3f-v2",
                    help='the step size of the program generation loop')
parser.add_argument('--policy_name', type=str, required=True,
                    help='the policy file name')
parser.add_argument('--test_prior_weighting', action='store_true',
                    help='test the weight for the prior decreasing from 1.0 to 0.0')
parser.add_argument('--test_same_program', action='store_true',
                    help='test the envs with the same LPP policy')
parser.add_argument('--test_with_stored_policy', action='store_true',
                    help='test the envs with the same LPP policy')
parser.add_argument('--test_number_of_demos', action='store_true',
                    help='test different number of demos')
args = parser.parse_args()
print('Train policy with args:', ' '.join(f'{k}={v}' for k, v in vars(args).items()))

ppl_file = f'policies/{args.policy_name}_ppl.pkl'

if args.test_number_of_demos is True:
    print('test number of demos')
    results = []
    n_demos = [1] + [p for p in range(5, 35, 5)] + [p for p in range(40, 70, 10)] + [80, 99]
    for nd in n_demos:
        policies = pipeline.train(args.env_name, range(nd), args.gen_prog_step_size,
                                  args.num_programs, args.num_dt, args.max_num_particles, 0.1)

        envs = ['Foraging-grid-5x5-2p-2f-v2']

        for i, e in enumerate(envs):
            rewards = []
            for d in range(100):
                rewards.append(run_foraging_policy(e, policies, render=False, max_demo_length=20*(i+1)))
            avg_reward = np.array(rewards).mean()
            std = np.array(rewards).std()
            print(f'n demos: {nd} env: {e}, avg. reward after run {d+1}: ' + str(avg_reward) + ' ' + str(std))
            results.append([e, nd, avg_reward, std])

    pd.DataFrame(results, columns=['env', 'n_demos', 'avg_reward', 'std']).to_csv(
        f'csv_results/results_n_demos_{args.policy_name}_ppl.csv')
    exit()

if args.test_with_stored_policy is True:
    results = []
    print(f'load policies from {ppl_file}')
    with open(ppl_file, 'rb') as f:
        policies = pickle.load(f)
    envs = ['Foraging-grid-5x5-2p-2f-v2', 'Foraging-grid-8x8-2p-4f-v2', 'Foraging-grid-10x10-2p-4f-v2', 'Foraging-grid-12x12-2p-4f-v2', 'Foraging-grid-14x14-2p-5f-v2', 'Foraging-grid-16x16-2p-6f-v2', 'Foraging-grid-18x18-2p-8f-v2',
            'Foraging-grid-5x5-3p-2f-v2', 'Foraging-grid-8x8-3p-4f-v2', 'Foraging-grid-10x10-3p-4f-v2', 'Foraging-grid-12x12-3p-4f-v2', 'Foraging-grid-14x14-3p-5f-v2', 'Foraging-grid-16x16-3p-6f-v2', 'Foraging-grid-18x18-3p-8f-v2',
            'Foraging-grid-5x5-4p-2f-v2', 'Foraging-grid-8x8-4p-4f-v2', 'Foraging-grid-10x10-4p-4f-v2', 'Foraging-grid-12x12-4p-4f-v2', 'Foraging-grid-14x14-4p-5f-v2', 'Foraging-grid-16x16-4p-6f-v2', 'Foraging-grid-18x18-4p-8f-v2',
            'Foraging-grid-5x5-5p-2f-v2', 'Foraging-grid-8x8-5p-4f-v2', 'Foraging-grid-10x10-5p-4f-v2', 'Foraging-grid-12x12-5p-4f-v2', 'Foraging-grid-14x14-5p-5f-v2', 'Foraging-grid-16x16-5p-6f-v2', 'Foraging-grid-18x18-5p-8f-v2',
            'Foraging-grid-5x5-6p-2f-v2', 'Foraging-grid-8x8-6p-4f-v2', 'Foraging-grid-10x10-6p-4f-v2', 'Foraging-grid-12x12-6p-4f-v2', 'Foraging-grid-14x14-6p-5f-v2', 'Foraging-grid-16x16-6p-6f-v2', 'Foraging-grid-18x18-6p-8f-v2']
    results = []

    for i, e in enumerate(envs):
        rewards = []
        for d in range(100):
            rewards.append(run_foraging_policy(e, policies, render=False, max_demo_length=20*(i+1)))
        avg_reward = np.array(rewards).mean()
        std = np.array(rewards).std()
        print(f'env: {e}, avg. reward after run {d+1}: ' + str(avg_reward) + ' ' + str(std))
        results.append([e, avg_reward, std])

    pd.DataFrame(results, columns=['env', 'avg_reward', 'std']).to_csv(
        f'csv_results/test_results_{args.policy_name}_ppl.csv')
    exit()

if args.test_same_program is True:
    print('test same program')
    results = []
    print(f'load policies from {ppl_file}')
    with open(ppl_file, 'rb') as f:
        pickle_policies = pickle.load(f)
    envs = ['Foraging-grid-5x5-2p-2f-v2', 'Foraging-grid-8x8-2p-4f-v2', 'Foraging-grid-10x10-2p-4f-v2', 'Foraging-grid-12x12-2p-4f-v2', 'Foraging-grid-14x14-2p-5f-v2', 'Foraging-grid-16x16-2p-6f-v2', 'Foraging-grid-18x18-2p-8f-v2',
            'Foraging-grid-5x5-3p-2f-v2',  # 'Foraging-grid-8x8-3p-4f-v2', 'Foraging-grid-10x10-3p-4f-v2', 'Foraging-grid-12x12-3p-4f-v2', 'Foraging-grid-14x14-3p-5f-v2', 'Foraging-grid-16x16-3p-6f-v2', 'Foraging-grid-18x18-3p-8f-v2',
            'Foraging-grid-5x5-4p-2f-v2',  # 'Foraging-grid-8x8-4p-4f-v2', 'Foraging-grid-10x10-4p-4f-v2', 'Foraging-grid-12x12-4p-4f-v2', 'Foraging-grid-14x14-4p-5f-v2', 'Foraging-grid-16x16-4p-6f-v2', 'Foraging-grid-18x18-4p-8f-v2',
            'Foraging-grid-5x5-5p-2f-v2',  # 'Foraging-grid-8x8-5p-4f-v2', 'Foraging-grid-10x10-5p-4f-v2', 'Foraging-grid-12x12-5p-4f-v2', 'Foraging-grid-14x14-5p-5f-v2', 'Foraging-grid-16x16-5p-6f-v2', 'Foraging-grid-18x18-5p-8f-v2',
            'Foraging-grid-5x5-6p-2f-v2']  # 'Foraging-grid-8x8-6p-4f-v2', 'Foraging-grid-10x10-6p-4f-v2', 'Foraging-grid-12x12-6p-4f-v2', 'Foraging-grid-14x14-6p-5f-v2', 'Foraging-grid-16x16-6p-6f-v2', 'Foraging-grid-18x18-6p-8f-v2']
    policies = [pickle_policies[0]] * len(pickle_policies)
    for i, e in enumerate(envs):
        rewards = []
        for d in range(100):
            rewards.append(run_foraging_policy(e, policies, render=False, max_demo_length=20*(i+1)))
        avg_reward = np.array(rewards).mean()
        std = np.array(rewards).std()
        print(f'env: {e}, avg. reward after run {d+1}: ' + str(avg_reward) + ' ' + str(std))
        results.append([e, avg_reward, std])
    pd.DataFrame(results, columns=['env', 'avg_reward', 'std']).to_csv(
        f'csv_results/results_same_program_{args.policy_name}_ppl.csv')
    exit()

if args.test_prior_weighting is True:
    print('test prior weighting')
    results = []
    prior_weights = [p / 10 for p in range(11)]
    for prior_weight in prior_weights:
        policies = pipeline.train(args.env_name, range(args.n_demos), args.gen_prog_step_size,
                                  args.num_programs, args.num_dt, args.max_num_particles, prior_weight)

        envs = ['Foraging-grid-5x5-2p-2f-v2']

        for i, e in enumerate(envs):
            rewards = []
            for d in range(100):
                rewards.append(run_foraging_policy(e, policies, render=False, max_demo_length=20*(i+1)))
            avg_reward = np.array(rewards).mean()
            std = np.array(rewards).std()
            print(f'prior weight: {prior_weight} env: {e}, avg. reward after run {d+1}: ' +
                  str(avg_reward) + ' ' + str(std))
            results.append([e, prior_weight, avg_reward, std])

    pd.DataFrame(results, columns=['env', 'prior_weight', 'avg_reward', 'std']).to_csv(
        f'csv_results/results_prior_weighting_{args.policy_name}_ppl.csv')

else:
    policies = pipeline.train(args.env_name, range(args.n_demos), args.gen_prog_step_size,
                              args.num_programs, args.num_dt, args.max_num_particles, 0.1)

    print(f'saved policies to {ppl_file}')
    with open(ppl_file, 'wb') as f:
        pickle.dump(policies, f)

    envs = ['Foraging-grid-5x5-2p-2f-v2', 'Foraging-grid-8x8-2p-4f-v2', 'Foraging-grid-10x10-2p-4f-v2', 'Foraging-grid-12x12-2p-4f-v2', 'Foraging-grid-14x14-2p-5f-v2', 'Foraging-grid-16x16-2p-6f-v2', 'Foraging-grid-18x18-2p-8f-v2',
            'Foraging-grid-5x5-3p-2f-v2', 'Foraging-grid-8x8-3p-4f-v2', 'Foraging-grid-10x10-3p-4f-v2', 'Foraging-grid-12x12-3p-4f-v2', 'Foraging-grid-14x14-3p-5f-v2', 'Foraging-grid-16x16-3p-6f-v2', 'Foraging-grid-18x18-3p-8f-v2',
            'Foraging-grid-5x5-4p-2f-v2', 'Foraging-grid-8x8-4p-4f-v2', 'Foraging-grid-10x10-4p-4f-v2', 'Foraging-grid-12x12-4p-4f-v2', 'Foraging-grid-14x14-4p-5f-v2', 'Foraging-grid-16x16-4p-6f-v2', 'Foraging-grid-18x18-4p-8f-v2',
            'Foraging-grid-5x5-5p-2f-v2', 'Foraging-grid-8x8-5p-4f-v2', 'Foraging-grid-10x10-5p-4f-v2', 'Foraging-grid-12x12-5p-4f-v2', 'Foraging-grid-14x14-5p-5f-v2', 'Foraging-grid-16x16-5p-6f-v2', 'Foraging-grid-18x18-5p-8f-v2',
            'Foraging-grid-5x5-6p-2f-v2', 'Foraging-grid-8x8-6p-4f-v2', 'Foraging-grid-10x10-6p-4f-v2', 'Foraging-grid-12x12-6p-4f-v2', 'Foraging-grid-14x14-6p-5f-v2', 'Foraging-grid-16x16-6p-6f-v2', 'Foraging-grid-18x18-6p-8f-v2']
    results = []

    for i, e in enumerate(envs):
        rewards = []
        for d in range(100):
            rewards.append(run_foraging_policy(e, policies, render=False, max_demo_length=20*(i+1)))
        avg_reward = np.array(rewards).mean()
        std = np.array(rewards).std()
        print(f'env: {e}, avg. reward after run {d+1}: ' + str(avg_reward) + ' ' + str(std))
        results.append([e, avg_reward, std])

    pd.DataFrame(results, columns=['env', 'avg_reward', 'std']).to_csv(
        f'csv_results/results_{args.policy_name}_ppl.csv')
