<h1 align='center'>  ROSSMANN STORES - SALES PREDICT </h1>

<div align=center>

![Rossmann](images/rossmann.jpg 'Logo Rossmann')
</div>


<p align="justify"><i>Esse é um problema de negócio fictício, porém a empresa e os dados são reais assim como a solução do problema também é feita seguindo os passos que um projeto real seguiria.</i></p>

<p align="justify"><i>Este README apresenta um apanhado dos métodos utilizados e dos principais resultados obtidos. Você pode obter mais detalhes visitando o 
<a href="https://github.com/MayconRochaaa/rossmann_project/blob/main/store_sales_prediction.ipynb">Jupyter Notebook</a> do projeto.</i></p>

# 1.0 - **Problema de negócio**

## 1.1 - **Descrição do problema**

<p align="justify"> A rede Rossmann opera mais de 3.000 farmácias em 7 países europeus. Atualmente, os gerentes das lojas Rossmann têm a tarefa de prever suas vendas diárias com até seis semanas de antecedência. As vendas das lojas são influenciadas por muitos fatores, incluindo promoções, competição, férias escolares e estaduais, sazonalidade e localidade. Com milhares de gerentes individuais prevendo vendas com base em suas circunstâncias únicas, a precisão dos resultados pode ser bastante variada. </p>

## 1.2 - **Objetivos**

<p align="justify">Como cientista de dados foi nos dado a tarefa de prever suas vendas diárias com até seis semanas de antecedência com uma precisão mais assertiva utilizando dados os dados disponíveis das lojas Rossmann. Além disso também foi solicitado a criação um Bot no aplicativo Telegram para que o CFO da empresa tenha acesso de maneira simples e remota às predições de vendas.</p>

## 1.3 - **Visão geral dos dados**

<p align="justify"> Os dados foram obtidos através da plataforma <a href="https://www.kaggle.com/c/rossmann-store-sales">Kaggle</a>. Neles temos informações de vendas de 1.115 lojas Rossmann entre os anos de Jan/2013 e Jul/2015. O dataset original contém as seguintes informações:</p>

<details><summary><strong> Descrição dos dados disponibilizados</strong> </summary>
    

| Variável                  | Descrição                                                                                                                                                                                          |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Id                        | Um ID que representa um par (Loja, Data) dentro do conjunto de teste.                                                                                                                             |
| Store                     | Um ID único para cada loja.                                                                                                                                                                       |
| Sales                     | O faturamento para um determinado dia (isso é o que você está prevendo).                                                                                                                         |
| Customers                 | O número de clientes em um determinado dia.                                                                                                                                                       |
| Open                      | Um indicador se a loja estava aberta: 0 = fechada, 1 = aberta.                                                                                                                                    |
| StateHoliday              | Indica um feriado estadual. Normalmente, todas as lojas, com poucas exceções, estão fechadas nos feriados estaduais. "a" = feriado público, "b" = feriado de Páscoa, "c" = Natal, "0" = Nenhum.       |
| SchoolHoliday             | Indica se (Loja, Data) foi afetado pelo fechamento das escolas públicas.                                                                                                                          |
| StoreType                 | Diferencia entre 4 modelos diferentes de lojas: "a", "b", "c", "d".                                                                                                                                 |
| Assortment                | Descreve o nível de sortimento: "a" = básico, "b" = extra, "c" = estendido.                                                                                                                        |
| CompetitionDistance       | Distância em metros até a loja concorrente mais próxima.                                                                                                                                          |
| CompetitionOpenSince[Month/Year] | Indica o ano e o mês aproximados em que o concorrente mais próximo foi aberto.                                                                                                                   |
| Promo                     | Indica se a loja está fazendo uma promoção naquele dia.                                                                                                                                           |
| Promo2                    | Promo2 é uma promoção contínua e consecutiva para algumas lojas: 0 = loja não está participando, 1 = loja está participando.                                                                    |
| Promo2Since[Year/Week]    | Descreve o ano e a semana do calendário em que a loja começou a participar do Promo2.                                                                                                           |
| PromoInterval             | Descreve os intervalos consecutivos em que o Promo2 é iniciado, nomeando os meses em que a promoção é iniciada novamente. Por exemplo, "Feb, May, Aug, Nov" significa que cada rodada começa em fevereiro, maio, agosto, novembro de qualquer ano para aquela loja.
</details>

# 2.0 - **Premissas do negócio**

- <p align="justify"> As colunas 'customers' e 'promo_interval' foram desconsideradas da análise, pois não é possível conhecer a quantidade de clientes ou por quanto tempo uma loja estará com promoção nas seis semanas futuras;</p>

- <p align="justify"> Os valores NaN na coluna de competition_distance serão preenchidos por 200000 metros, que representa uma distancia muito grande quado comparada com as demais no dataset;</p>

- <p align="justify"> No processo de Feature Engineering foi criado novas features julgadas relevantes para o problema:</p>

    <details><summary><strong> Features derivadas</strong> </summary>

    - Ano
    - Mês
    - Dia
    - Semana do ano
    - Ano-Semana
    - Tempo de competição
    - Tempo de competição por mês
    - Tempo de promoção
    - Tempo de promoção por semana
    - Alteração nos valores de assortment
    </details>


# 3.0 - **Estratégia de solução**

<p align="justify"> A estratégia de solução se baseia no método CRISP-DS que prioriza e agiliza a entrega de resultado e valor do projeto. O ciclo é representado pelo esquema abaixo:</p>

 <div align="center">

![CRISPDS](images/CRISPDS.jpg 'Ciclo CRISP-DS') 
</div>

- <p align="justify"><strong>Business Problem e Business Understanding</strong>: Etapa inicial, recebemos o problema e procuramos entender as motivações que levaram o CFO solicitar a tarefa e com base nisso elaboramos uma estratégia de solução;</p>

- <p align="justify"><strong>Data Extraction</strong>: Coleta dos dados das lojas Rossmann no site Kaggle;</p>

- <p align="justify"><strong>Data Cleaning</strong>: Aqui as colunas do dataset são renomeadas no modelo snake_case; analisamos e alteramos o tipo das variáveis quando necessário; preenchimento dos valores NaN com base no conhecimento do negócio;</p>
    
    <p align="justify">Neste processo também é realizado a etapa de <strong>Feature Engineering</strong>, onde derivamos novas features a partir das originais. As novas features são criadas a partir da tentativa de validar hipóteses levantadas sobre os negócio;</p>

- <p align="justify"><strong>Exploratory Data Analysis (EDA)</strong>: A etapa mais importante de qualquer projeto de Data Science. Aqui vamos verificar a validade das hipóteses levantadas e obter insights do negócio. Ela foi dividida em três partes: análise univariada, bivariada e multivariada;</p>


- <p align="justify"><strong>Modeling</strong>: Nesta etapa os dados foram trabalhados para que possam performar melhor quando o modelo de ML for implementado. Este processo visa deixar todas variáveis numéricas em uma escala "justa", aplicando técnicas de normalização e reescalonamento, para que nenhuma feature tenha mais relevância que outra no modelo de ML; aplicar técnicas de encoding nas variáveis categóricas e transformações de natureza nas features e na variável resposta.</p>

    <p align="justify">Nesta etapa também é feito o processo de <strong>Feature Selection</strong>, onde selecionamos apenas as variáveis relevantes para o modelo, com base nos resultados do processo de EDA e também aplicando o algoritmo <strong>Boruta</strong>;</p>


- <p align="justify"><strong>Machine Learning Algorithms</strong>: Treinamento do modelo utilizando diferentes algoritmos de regressão e aplicando o método de <strong>Cross-Validation</strong> modificado para séries temporais;</p>

- <p align="justify"><strong>Evaluation</strong>: É escolhido o algoritmo com melhor performance na etapa anterior com base nas métricas: MAE, MAPE, RMSE e R². Além disso também é feito a tradução desses resultados em termos de performance de negócio;</p>

- <p align="justify"><strong>Deployment</strong>: É criado uma API utilizando a plataforma <strong>Render</strong>, isso possibilita que qualquer pessoa possa utilizar o modelo para prever as vendas de uma loja Rossmann. Para criar uma interface mais amigável e acessível utilizou-se a API do Telegram Bot para criar um Chat Bot no aplicativo Telegram;</p>

- <p align="justify"><strong>Novo ciclo</strong>: Após o projeto entrar em produção o ciclo se repete, visando aperfeiçoar a performance do modelo.</p>

## 3.1 Ferramentas utilizadas

<div align="center">

|    <!-- -->   |                    <!-- -->                     |
|---------------|-------------------------------------------------|
|**Programação**| Python 3.11.3; <br> Jupyter Notebook; <br> VSCode. |
|**Visualização de dados**|   Matplotlib; Seaborn.  |
|**Bibliotecas de ML**|Sklearn; Xgboost; Boruta.|
|**Engenharia de software**| Flask; <br> Git; Github; <br> Render Cloud; Telegram Bot.|

</div>

# 4.0 - **Principais insights**

## 4.1 Lojas com competidores mais próximos vendem menos

<div align=center>

![H2](images/H2.png 'sadas')
</div>

## 4.2 Lojas vendem menos durante os feriados escolares.

<div align=center>

![H13](images/H13.png 'sadas')
</div>

## 4.3 Lojas vendem menos aos finais de semana.

<div align=center>

![H12](images/H12.png 'sadas')
</div>

# 5.0 - **Modelos de Machine Learning**

<p align="justify">Foram testados cinco modelos de ML, dois lineares: Regressão linear (LR) e Regressão Linear Regularizada (LASSO); duas não lineares: Random Forest Regressor (RFR) e XGBoost Regressor (XGB) e por ultimo o Average Model, utilizado como base para comparar a performance dos demais modelos. As métricas de performance são o MAE, MAPE, RMSE e R² que são definidas como:</p>

<div align="center">

| Métrica |                Definição               |
|:-------:|:--------------------------------------:|
|   MAE   |          Erro absoluto médio           |
|   MAPE  |        Erro absoluto médio percentual  | 
|   RMSE  |Raiz quadrática do erro quadrático médio|
|    R²   |       Coeficiente de determinação      |

</div>

 <p align="justify">O MAE e MAPE conseguem explicar o desempenho comercial do modelo. O MAE mostra o quanto a previsão do modelo está errada, em média; já o MAPE tem interpretação semelhante, mas em termos percentuais. O RMSE e R² não possuem uma interpretação útil do ponto de vista financeiro, entretanto são elas que nos dizem o quão bom nosso modelo descreve o fenômeno, quanto menor o RMSE e maior R² melhor é a performance do modelo.</p>


 <p align="justify">Abaixo a performance desses modelos aplicando o método de Cross-Validation, ordenando pelo RMSE:</p>

  <div align="center">

|Model Name|         MAE        |  MAPE (%) |       RMSE       |   R² (%)   |
|:---------|:------------------:|:---------:|:----------------:|:----------:|
|   RFR	   |   837.1 +/- 217.71 | 12 +/- 2  | 1256.4 +/- 319.0 |  84 +/- 05 |
|   XGB    | 1076.27 +/- 199.96 | 15 +/- 2  | 1541.7 +/- 278.4 |  76 +/- 03 |
|Average Model| 1354.8          |    21     |       1835.1     |     64     |
|   LR     | 2081.73 +/- 295.63 | 30 +/- 2  | 2952.5 +/- 468.4 |  14 +/- 07 |
|   LASSO  | 2388.68 +/- 398.48 | 34 +/- 1  | 3369.4 +/- 567.5 | -12 +/- 11 |
</div>

<p align="justify">Os dois métodos lineares apresentam os piores resultados, apresentando um RMSE menor que o Average Model. Isso demonstra que a complexidade do dataset não pode ser bem descrita por métodos lineares de regressão. Resta então os modelos não lineares, que apresentaram uma performance semelhante, embora a RFR apresente um menor RMSE seguiremos com o XGB regressor devido ao desempenho semelhante, mas principalmente pelo menor tempo de processamento quando comparado com o RFR.</p>

<p align="justify">Após ter escolhido o modelo agora é  necessário refina-lo para obter uma performance ainda melhor. Existem diferentes formas de fazer isso, neste projeto foi utilizado a Random Search que, aleatoriamente, procura os parâmetros do modelo que apresentam a melhor performance. Feito isso obtemos as seguintes métricas:</p>

<div align="center">

| Model Name |  MAE  |  MAPE (%) |       RMSE       |   R² (%)   |
|:----------:|:-----:|:---------:|:----------------:|:----------:|
|     XGB    | 655.8 |	  9.5    |	     950.6      |     90     |
</div>

## 5.1 Performance do ponto de vista financeiro:

A seguir é exibido o resultado das previsões em termos financeiros das próximas seis semanas, preditos utilizando o modelo XGBoost. Na primeira tabela temos os resultados de cinco lojas, na segunda previsões de toda a receita das lojas Rossmann: 

<div align="center">PREVISÕES DE CINCO LOJAS ROSSMANN

| store |predictions (€)|worst_scenario (€)|best_scenario (€)| MAE (€) |MAPE (%)|
|:-----:|:-------------:|:----------------:|:---------------:|:-------:|:------:|
|   1   |   160918.3    |     160605.4     |     161231.3    |  312.98 |  7.13  |
|   2   |   172913.7    |     172558.8     |     173268.7    |  354.93 |  7.13  |
|   3   |   259753.0    |     259133.0     |     260373.1    |  620.05 |  8.70  |
|   4   |   342506.6    |     341580.2     |     343433.0    |  926.40 |  8.84  |
|   5   |   176090.4    |     175639.8     |     176540.9    |  450.55 |  9.85  |

</div>


<div align="center">PREVISÃO DA RECEITA TOTAL DAS LOJAS ROSSMANN


|**Scenarios**:|  predictions   | worst_scenario   | best_scenario |
|:-------:|:--------------:|:----------------:|:-------------:|
|**Values**:|€282,487,520.00 | €281,752,205.36  |€283,222,827.51|
</div>


# 6.0 - **Produto final**

<p align="justify">Para disponibilizar esses resultados de forma prática e remota foi criado a <a href="https://github.com/MayconRochaaa/webapp_rossmann">API-Rossmann</a>
utilizando a biblioteca Flask e feito o deploy na plataforma Render. Essa API se comunica a API do Telegram Bot, permitindo que solicitações sejam envias através de uma mensagem de texto para um Chat Bot no aplicativo Telegram, que retorna as informações da loja escolhida na mensagem. Para solicitar a informação de uma loja o usuário deve enviar uma mensagem do tipo "/[número da loja]" sem as chaves, caso a loja não exista uma mensagem será enviada ao usuário informando isso; caso o texto não esteja no formato para realiza a solicitação o bot irá retornar uma mensagem solicitando um ID válido.</p>

<p align="justify">Você pode acessar o Chat Bot clicando no link abaixo. A primeira consulta pode não ser respondida instantaneamente.</p>

 <div align="center">

[![image](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/maycon_rossmann_bot)
</div>

# 7.0 - **Conclusões**

<p align="justify">O primeiro ciclo do CRISP-DS foi concluído com sucesso, passamos por todas etapas essências de um projeto real de ciência de dados. Obtemos insights preciosos sobre as vendas das lojas Rossmann durante o processo de EDA, que possibilitou definir um conjunto de features que entrega uma performance satisfatória ao utilizar o modelo XGBoost Regressor, possibilitando predições mais precisas das vendas das lojas da rede Rossmann nas seis semanas futuras.</p>

<p align="justify">O modelo foi colocado em produção e desenvolvido um Chat Bot que possibilita a consulta de forma remota da previsão de vendas das lojas Rossmann, sendo necessário apenas uma conexão com a internet.</p>

# 8.0 - **Próximos passos**

<p align="justify">A performance do modelo ainda possuí margem para ser aprimorada ainda mais. Ao iniciar um novo ciclo do CRISP-DS podemos abordar as seguintes estratégias:</p>

- <p align="justify">Elaborar mais hipóteses sobre o negócio para gerar mais Features que podem ser relevantes para descrever o problema;</p> 

- <p align="justify">Desenvolver um segundo modelo capaz de prever o número de clientes na próximas seis semanas, para que não seja necessário excluir a coluna 'costumers' do dataset;</p> 

- <p align="justify">Aplicar o método de otimização bayesiana para realizar o Hyperparameter Fine Tunnig;</p> 

- <p align="justify">Testar diferentes algoritmos de Machine Learning;</p> 

- <p align="justify">Adicionar novos comandos e interações no Chat Bot.</p> 

# Contato: [![LinkedIn](https://img.shields.io/badge/-LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mayconrocha14/)  [![Gmail](https://img.shields.io/badge/-Gmail-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:mayconrochads@gmail.com)  [![Discord](https://img.shields.io/badge/-Discord-5865F2?style=flat-square&logo=discord&logoColor=white)](https://discord.com/users/Marimbondo#7836)


