import copy
class Setting:
    CT_types_list = []

    #Trong list này có 3 list nhỏ. Mỗi list là một danh sách các CT type được thử nghiệm. Mỗi CT type là một list gồm 3 phần tử: [size, CI, delay_requirement]
    CT_types_sysload_experiment = [
        [
            [500000, 40, 0.02],
            [1000000, 40, 0.02],
            [1500000, 40, 0.02],
            [2000000, 40, 0.02],
            [2500000, 40, 0.02]
        ],
        [
            [1500000, 10, 0.02],
            [1500000, 20, 0.02],
            [1500000, 40, 0.02],
            [1500000, 60, 0.02],
            [1500000, 100, 0.02]
        ],
        [
            [2000000, 10, 0.03],
            [2000000, 20, 0.03],
            [2000000, 40, 0.03],
            [2000000, 60, 0.03],
            [2000000, 100, 0.03]
        ]
    ]

    CT_types_numtasks_experiment = copy.deepcopy(CT_types_sysload_experiment)
    CT_types_CI_experiment = copy.deepcopy(CT_types_sysload_experiment)
    CT_types_size_experiment = copy.deepcopy(CT_types_sysload_experiment)
    CT_types_delay_experiment = copy.deepcopy(CT_types_sysload_experiment)
    CT_types_accuracy_experiment = copy.deepcopy(CT_types_sysload_experiment)
    
    # CT_types_numtasks_experiment = [
    #     [
    #         [500000, 40, 0.02],
    #         [1500000, 40, 0.02],
    #         [1500000, 40, 0.02],
    #         [2000000, 40, 0.02],
    #         [2500000, 40, 0.025]
    #     ],
    #     [
    #         [1500000, 10, 0.01],
    #         [1500000, 20, 0.01],
    #         [1500000, 40, 0.01],
    #         [1500000, 60, 0.01],
    #         [1500000, 100, 0.01]
    #     ],
    #     [
    #         [2000000, 10, 0.03],
    #         [2000000, 20, 0.03],
    #         [2000000, 40, 0.03],
    #         [2000000, 60, 0.03],
    #         [2000000, 100, 0.03]
    #     ]
    # ]

    # CT_types_CI_experiment = [
    #     [
    #         [500000, 40, 0.02],
    #         [1500000, 40, 0.02],
    #         [1500000, 40, 0.02],
    #         [2000000, 40, 0.02],
    #         [2500000, 40, 0.025]
    #     ],
    #     [
    #         [1500000, 10, 0.01],
    #         [1500000, 20, 0.01],
    #         [1500000, 40, 0.01],
    #         [1500000, 60, 0.01],
    #         [1500000, 100, 0.01]
    #     ],
    #     [
    #         [2000000, 10, 0.03],
    #         [2000000, 20, 0.03],
    #         [2000000, 40, 0.03],
    #         [2000000, 60, 0.03],
    #         [2000000, 100, 0.03]
    #     ]
    # ]

    # CT_types_size_experiment = [
    #     [
    #         [500000, 40, 0.02],
    #         [1500000, 40, 0.02],
    #         [1500000, 40, 0.02],
    #         [2000000, 40, 0.02],
    #         [2500000, 40, 0.025]
    #     ],
    #     [
    #         [1500000, 10, 0.01],
    #         [1500000, 20, 0.01],
    #         [1500000, 40, 0.01],
    #         [1500000, 60, 0.01],
    #         [1500000, 100, 0.01]
    #     ],
    #     [
    #         [2000000, 10, 0.03],
    #         [2000000, 20, 0.03],
    #         [2000000, 40, 0.03],
    #         [2000000, 60, 0.03],
    #         [2000000, 100, 0.03]
    #     ]
    # ]

    # CT_types_delay_experiment = [
    #     [
    #         [500000, 40, 0.02],
    #         [1500000, 40, 0.02],
    #         [1500000, 40, 0.02],
    #         [2000000, 40, 0.02],
    #         [2500000, 40, 0.025]
    #     ],
    #     [
    #         [1500000, 10, 0.01],
    #         [1500000, 20, 0.01],
    #         [1500000, 40, 0.01],
    #         [1500000, 60, 0.01],
    #         [1500000, 100, 0.01]
    #     ],
    #     [
    #         [2000000, 10, 0.03],
    #         [2000000, 20, 0.03],
    #         [2000000, 40, 0.03],
    #         [2000000, 60, 0.03],
    #         [2000000, 100, 0.03]
    #     ]
    # ]


        

