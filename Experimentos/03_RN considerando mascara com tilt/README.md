# RN considerando mascara com tilt
Treinamento e analise da técnica de Rede Neural considerando uma entrada com Tilt em dois aplificadores diferentes.

## Passo a Passo

Siga as instruções a seguir para chegar até os resultados com cada pasta possuindo os scripts espelhados, quando não será comentado.

### Pré-requisitos

Verifique se sua máquina possui python e os módelos.

* Python 3
* Keras
* TensorFlow
* Numpy
* Glob
* Matplotlib
* Pickle

## Preparação dos dados
Para tratar os dados será necessário seguir a sequência de arquivos a baixo.

### 1 - joinAllResults.py
Sua função é ler todos as máscaras que estão na pasta do aplificador específico, exemplo "EDFA_1STG", e transformar em um grande arquivo contendo os dados delas.

### 2 - transformMaskFileFromOptToSim.py
Tira as informações que não serão utilizadas da máscara pura.

### 3 - formatDataToICTON17.py e formatDataToNewModels.py
Estrutura os dados para a morfologia de rede especificada em seu nome.

### 4 - normalizeICTON17Data.py e normalizeNewModelsData.py
Normaliza e guarda as informações necessárias para desnormalização em um arquivo.

### 5 - splitDataIntoKFolds.py
Divide os dados em 5 folds de forma aleatória mas mantendo a consistência entre os modelos diferentes.

## Treinamento dos modelos

Cada modelo é treinado em um script diferente para ter a possibilidade do treinamento em paralelo.
São criados 5 instâncias do mesmo modelo onde são utilizadas 4 folds para treinamento e 1 fold para teste, alternando sua função para cada instância. 

### NN-icton17-o.py
Modelo apresentado na literatura para predição de uma máscara plana.

### NN-icton17.py
Modelo simular ao da literatura adicionando a informação de tilt.

### NN-41to40.py
Modelo com a morfologia proposta com 41 entradas e 40 saídas.

### NN-42to40.py
Similar a anterior adicionando uma entrada a mais, que é a informação do tilt.

## Apresentação dos resultados

Os resultados são apresentados em boxplots. São utilizadas a métrica da média dos erros das entradas e do maior erro de cada entrada.

### errorWithBoxplot.py
Cria os gráficos com boxplot da média dos erros das entradas. Utilizando para calcular os folds de testes respectivos para as instâncias de cada modelo.

### biggestErrorWithBoxplot.py
Igualmente a anteior porém utilizando o maior erro de cada entrada.


## Método da interpolação

## Comparação com menos máscaras
