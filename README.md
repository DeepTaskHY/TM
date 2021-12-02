# 1. Test Manager

## 2. Package summery 

This module is for demonstration at Hanyang University.

- 2.1 Maintainer status: maintained
- 2.2 Maintainer: Eunsoo Lee ([eunsoogi@hanyang.ac.kr]())
- 2.3 Author: Eunsoo Lee ([eunsoogi@hanyang.ac.kr]())
- 2.4 License (optional): 
- 2.5 Source git: https://github.com/DeepTaskHY/TM

## 3. Environments

- [ros:noetic](https://hub.docker.com/layers/ros/library/ros/noetic/images/sha256-c1565b2b554d775f1fb2fde93d1aaf76554a6a98d06f10432b0dd4ddd5d6a11c)
- Python 3.7+

## 4. Quick start

### 4.1 Clone the module

This module contains submodules. When using this module, all submodules must be checked out.

```shell
git clone --recursive https://github.com/DeepTaskHY/TM
```

### 4.2 Setup the module

There are submodules that require configuration. Environment setting is required for each submodule.

#### 4.2.1 [Planning Manager](modules/PM)

This submodule does not require any configuration.

#### 4.2.2 [[M2-6] Dialogue Generator](modules/DM_Generator)

This submodule is required to set a configuration and download the secret key used by an external module. Click [this link](https://github.com/DeepTaskHY/DM_Generator#5-quick-start) to see how to configure it.

#### 4.2.3 [[M2-7] Intention Classifier](modules/DM_Intent)

This submodule is required to download the model checkpoint and the secret key used by an external module. Click [this link](https://github.com/DeepTaskHY/DM_Intent_2#5-quick-start) to see how to configure it.

#### 4.2.4 [[M2-8] Social Ontology Model](modules/KM)

This submodule does not require any configuration.

#### 4.2.5 [Vision](modules/Vision)

This submodule does not require any configuration.

#### 4.2.6 [Speech](modules/Speech)

This submodule does not require any configuration.
