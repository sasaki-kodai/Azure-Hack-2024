# Azure-Hack-2024

## ローカルの環境構築
### pythonの設定
pyenv+virtualenv+poetryで行っている

macOS想定(azure-search-documentsが入らなかったのでubuntuに移行)

VS codeをインストールしておく、ExtensionsでAzure Toolsを入れる


1. ```pyenv```をgithubから```$HOME```配下に持ってくる
```sh
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```
2. ```pyenv```の環境変数の設定を```.bash_profile```に書き込む。
```sh
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"

```
3.  ```pyenv```コマンドが使えることを確認する
```sh
pyenv -v
# pyenv 2.1
```
4.  ```pyenv```経由でpythonをインストール
```sh
pyenv install --list
pyenv install 3.11.9
```
5.  デフォルトで使用するpythonのバージョンを切り替える
```sh
pyenv global 3.11.9
pyenv versions
#   system
# * 3.11.8 (set by /home/masaya_kondo/.pyenv/version)
```
6.  pipでvirtualenvをインストールする
```sh
pip install virtualenv
```
7.  virtualenvコマンドでpythonの仮想環境を作成する。以下はdevという名前の仮想環境を作成する

仮想環境はvirtualenvコマンドを実行したディレクトリ直下に仮想環境名のフォルダが作成される
```sh
virtualenv env
```
8.  作成した仮想環境を有効にする
```sh
source env/bin/activate
```
9. poetryをインストール
```sh
pip install poetry
```

### プロジェクトの環境構築

11. このプロジェクトをgit cloneしてくる
```sh
git clone https://github.com/sasaki-kodai/Azure-Hack-2024.git
```
12. ライブラリを持ってくる
プロジェクト配下にあるpoetry.lockに従って環境が構築される
```sh
poetry install --no-root
```
ライブラリを追加したい場合は、下記で持ってくる
```sh
poetry add hogehoge
```
13. Azure CLIをインストール(ubuntuでは入れてない)
https://learn.microsoft.com/ja-jp/dotnet/azure/install-azure-cli

### jupyterの設定

上記の設定のままだとvirtualenvの環境をjupyter lab等で使えないので、jupyter labで仮想環境が使えるように設定する

下記の手順はvirtualenvで仮想環境を作成する度に必要
1. virtualenvの仮想環境にいる状態でipykernelをインストールする
```sh
poetry add ipykernel
```
2. jupyterに仮想環境のkernelを追加する
```sh
ipython kernel install --user --name=仮想環境名
```
これでipynbを立ち上げたときに右上に表示されるカーネルのところに、さっき構築した仮想環境が選択できるようになる