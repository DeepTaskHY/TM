# 1. Test Manager

## 2. Package summery 

This module is for demonstration at Hanyang University.

- 2.1 Maintainer status: maintained
- 2.2 Maintainer: Eunsoo Lee ([eunsoogi@hanyang.ac.kr]()), Gunhee Cho ([freebeinq@gmail.com]())
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
$ git clone --recursive https://github.com/DeepTaskHY/TM
```

When the submodule is updated, use the following command.

```shell
$ git submodule update --remote
```

### 4.2 Setup the module

There are submodules that require configuration. Environment setting is required for each submodule.

#### 4.2.1 [Planning Manager](modules/PM)

This submodule does not require any configuration.

#### 4.2.2 [[M2-6] Dialogue Generator](modules/DM_Generator)

This submodule is required to set a configuration and download the secret key used by an external module. Click [this link](https://github.com/DeepTaskHY/DM_Generator#5-quick-start) to see how to configure it.

#### 4.2.3 [[M2-7] Intention Classifier](modules/DM_Intent)

This submodule is required to download the secret key used by the external module. Click [this link](https://github.com/DeepTaskHY/DM_Intent_2#5-quick-start) to see how to configure it.

#### 4.2.4 [[M2-8] Social Ontology Model](modules/KM)

This submodule does not require any configuration.

#### 4.2.5 [Vision](modules/Vision)

This submodule should set the index of the camera device to be connected. Check the camera list using the following command.

```shell
$ sudo apt install v4l-utils
$ v4l2-ctl --list-devices
```

#### 4.2.6 [Speech](modules/Speech)

This submodule needs to set the index of the microphone device to be connected. Check the list of microphones using the following command.

```shell
sudo apt install libportaudio2
python -m sounddevice
```

### 4.3. Start the module

This module supports `docker-compose`. You can run it using the following command.

```shell
$ docker-compose --env-file=.env up tm-default  # or
$ docker-compose --env-file=.env up tm-linux
```

You can configure the execution environment by editing the [environment file](.env).

```shell
$ cp .env.example .env
$ vi .env
```
