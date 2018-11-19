QUESTIONNAR MINING PROJECT Repository
========================
テキストマイニングでクラスターを作成するプログラムです。

インストール(git & git lfs)
----------
gitおよびgit lfsをインストールの後、以下のコマンドを実行してください。

- git clone git@github.com:AMDlab/questionnaire_mining.git
- cd questionnaire_mining
- git lfs pull


実行に必要な環境
----------
    - python3.5.0
    - Mecab
        インスートル(Windows):
            1. exeファイルを以下のリンクからダウンロードし、実行してください。
                https://github.com/ikegami-yukino/mecab/releases/tag/v0.996   

実行方法
----------
    0. resource/text_data　ファイルに分析したいデータを配置してください。
    1. 
        a. Windowsの場合:
            1. 以下のソースをダウンロードし、pip コマンドでインストールしてください。
                https://github.com/studio-ousia/mojimoji
            2. コマンドプロンプト上のこのリポジトリのルートで `pip install -r requirements_windows.txt`を入力してください。
        b. Macの場合:
            ターミナルこのリポジトリのルートで `pip install -r requirements_mac.txt` を入力してください。
    2. `python main.py` を入力して、プログラムを入力してください。
    3. `result`　ディレクトリの配下に分析の結果が出力されます。 


背亭
----------
setting.ymlの内容を変更することで、分析のための設定を変更することができます。

    - cluster_num 
        作成するクラスターの数 
    - default_except_keyword
        解析前の文書から除外しておく言語(半角で入力)
    - default_except_reg 
        解析前の文書から除外したいフレーズの正規表現(半角で入力)
    - except_keywords
        解析結果から除外させる単語
    - except_main_features
        除外する品詞1リスト ex.['記号', '助詞', '助動詞', '感動詞', '接頭詞', '副詞', '連体詞', '接続詞']
    - except_sub_features
        除外する品詞2リスト ex.['代名詞', '接尾','副詞可能', '自立', '非自立', '形容動詞語幹']
    - bias
        学習済みモデルデータに対するテストデータのバイアス


----------
----------

This is the repository for text mining.
We can analyse long sentence and divide lines into cluster

Install(git & git lfs)
----------
you need git and git lfs to install. Install them before install this program.  

- git clone git@github.com:AMDlab/questionnaire_mining.git
- cd questionnaire_mining
- git lfs pull

Requirement
----------
    - python3
    - Mecab
        install(Windows):
            1. Download exe file
                https://github.com/ikegami-yukino/mecab/releases/tag/v0.996     

To Execute
----------
    0. Put your text file into .resource/text_data to analyse it.
    1. Open Terminal (Command Prompt), move to this repository's root and...
        a. If your PC is Windows:
            1. Download data and install it with pip command
                https://github.com/studio-ousia/mojimoji
            2. Type `pip install -r requirements_windows.txt` to get Libraries.
        b. If your PC is Mac:
            Type `pip install -r requirements_mac.txt` to get Libraries.
    2. execute main method with the command `python main.py`
    3. After 2, the result is written on files in `result` 


Settings
----------
If you need to change the setting, you have to edit setting.yml

    - cluster_num 
        The number of cluster that you want to create.  
    - default_except_keyword
        The list of word which you want to exclude from resource text.
    - default_except_reg 
        The regexp to exclude words from text.
    - except_keywords
        The list of word which you want exclude from result.
    - except_main_features
        The list of first feature  which you want exclude from result.
        ex.['記号', '助詞', '助動詞', '感動詞', '接頭詞', '副詞', '連体詞', '接続詞']
    - except_sub_features
        The list of second feature  which you want exclude from result.
    - bias
        The strength of bias to study the resource text.
        Because this program is using leaned model, we have to deicide the weight for leaned model and resource text.
