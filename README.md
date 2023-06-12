# PROJETO: ROSSMANN STORE - SALES PREDICT

A rede Rossmann opera mais de 3.000 farmácias em 7 países europeus. Atualmente, os gerentes das lojas Rossmann têm a tarefa de prever suas vendas diárias com até seis semanas de antecedência. As vendas das lojas são influenciadas por muitos fatores, incluindo promoções, competição, férias escolares e estaduais, sazonalidade e localidade. Com milhares de gerentes individuais prevendo vendas com base em suas circunstâncias únicas, a precisão dos resultados pode ser bastante variada. Como cientista de dados foi nos dado a tarefa de prever suas vendas diárias com até seis semanas de antecedência com uma precisão mais assertiva utilizando dados os dados disponíveis das lojas Rossmann.

Esse é um problema fictício, onde os dados são de uma competição na plataforma [Kaggle](https://www.kaggle.com/c/rossmann-store-sales), entretanto a solução do problema é feita seguindo os passos que um projeto real segue.

## 1.0 PROBLEMA DE NEGÓCIO

### 1.1 Descrição do problema

Algumas lojas da rede Rossmann necessitam passar por reformas, para entender melhor a viabilidade desse investimento o CFO da rede precisa ter conhecimento do como as lojas vão vender nas próximas seis semanas. Para isso foi disponibilizado ao time de ciência de dados uma base de dados históricos de vendas de 1.115 lojas Rossmann entre Jan/2013 e Jul/2015. Para facilitar o acesso do CFO a essas informações também foi solicitado a elaboração de um bot no app Telegram, em que seja possível verificar a previsão de faturamento de uma loja indicando no chat o número da loja em questão.

### 1.2 Objetivos

O projeto tem como objetivo elaborar um modelo de machine learning que seja capaz de descrever bem o comportamento de vendas das lojas presentes na base de dados e consequentemente realizar predição precisas das vendas de cada loja nas próximas seis semanas a partir da data de consulta.

Como meio de tornar essas previsões acessíveis ao CFO também deve-se criar um bot no app Telegram que informa essas previsões a partir de uma consulta de determinada loja.

<details><summary><strong> 1.3 Descrição dos dados disponibilizados</strong> </summary>
    

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

## 2.0 PREMISSAS DO NEGÓCIO

- Os dias em que as lojas estavam fechadas foram desconsiderados;
- Lojas com vendas iguais a zero não foram consideradas;
- Lojas que não possuem informação de competidores próximos foram preenchidas por 200000 metros

## 3.0 PLANEJAMENTO DA SOLUÇÃO

O projeto seguiu a metodologia CRISP-DS que prioriza e agiliza a entrega de resultado e valor do projeto. O processo segue o esquema abaixo:![CRISP-DS](images/CRISPDS.jpg "Ciclo CRISP-DS")

### 3.1 Problema de negócio e Entendimento
Essas etapas já foram abordadas na seção 1.0.

### 3.2 Extração de dados
Neste trabalho os dados foram fornecidos através da plataforma Kaggle.

### 3.3 Limpeza dos dados

Nessa etapa ocorre o primeiro contato com os dados, onde é feita alterações gerais e análises mais superficiais no dataset para se obter uma visão geral dos dados.

#### 3.3.1 Descrição dos dados

Foi feito uma padronização das colunas colocando-as em Snake Case; preenchimento dos valores vazios com base no conhecimento do negócio; correção dos tipos de variáveis nas colunas e também foi feita uma análise estatística descritiva dos dados.

O conjunto de dados após esses processos passa a ser composto por 1017209 linhas e 18 colunas.

#### 3.3.2 Feature Engineering

Em seguida iniciou-se o processo de criação de novas features, derivadas das originais, que podem agregar valor para o modelo de Machine Learning. Para isso criou-se um mapa mental de hipóteses sobre o negócio e com base nelas foram derivadas as variáveis necessárias para responde-las. As hipóteses levantadas que podem ser respondidas com os dados do dataset estão listadas abaixo.

<details><summary><strong> Hipóteses selecionadas</strong> </summary>

**1.** Lojas com maior sortimento deveriam vender mais;

**2.** Lojas com competidores mais próximos deveriam vender menos;

**3.** Lojas com competidores à mais tempo deveriam vender mais.

--------------------------------------------------------------------------------

**4.** Lojas que tem preços menores por mais tempo nos produtos deveriam vender mais.

**5.** Lojas com mais dias de promoção deveriam vender mais;

**6.** Lojas com mais promoções consecutivas deveriam vender mais.

--------------------------------------------------------------------------------

**7.** Lojas que abrem durante o natal deveriam vender mais;

**8.** Lojas deveriam vender mais ao longo dos anos;

**9.** Lojas deveriam vender mais no segundo semestre do ano;

**10.** Lojas deveria vender mais após o dia 10 de cada mês;

**11.** Lojas deveriam vender menos aos finais de semana;

**12.** Lojas deveriam vender menos durante feriados escolares;
</details>  

Para responder essas questões foram derivadas variáveis listadas a seguir: 

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

### 3.3.3 Filtragem de variáveis

Nesta etapa foi feita a exclusão de colunas e linhas do dataset com base nas restrições de negócio como dados que não estarão disponíveis no momento da predição (por exemplo, a coluna costumers, que não tem como saber a quantidade de clientes estarão na loja nas próximas seis semanas) ou ainda que não agregam informação para o modelo.

- Foram considerados apenas lojas que tiveram venda diferente de zero e as que não estavam fechadas;

- As colunas 'costumers', 'open', 'promo_interval' e 'month_map' foram excluídas.

## 3.4 ANALISE EXPLORATÓRIA DOS DADOS

A etapa mais importante de qualquer projeto de Data Science. Aqui vamos verificar a validade das hipóteses levantadas e obter insights do negócio. Ela foi dividida em três partes: análise univariada, bivariada e multivariada.

- **Análise univariada**: Nesta etapa analisamos cada variável individualmente, inclusive a variável target ('sales'), observando como se comporta sua curva de distribuição por exemplo.
- **Análise bivariada**: Aqui verificamos como nossas features se comportam com relação a variável resposta, isso é feito verificando a validade das hipóteses levantadas anteriormente.
- **Análise multivariada**: Nesse momento é feito uma análise de como cada feature se relaciona com as demais, esse processo é feito através de uma análise de correlação entre as variáveis. Esse processo é importante para reduzir a dimensionalidade do dataset e consequentemente sua complexidade, pois nos mostra se uma variável possui correlação forte com as demais, de modo que as que são fortemente correlacionadas podem ser descartadas sem grandes perdas posteriores na aplicação do modelo de ML.

## 3.5 Modelagem

### 3.5.1 Preparação dos dados

Nesta etapa os dados foram trabalhados para que possam performar melhor quando o modelo de ML for implementado. Este processo visa deixar todas variáveis em uma escala "justa", para que nenhuma feature tenha mais relevância que outra.

Variáveis numéricas que apresentam uma distribuição gaussiana serão normalizadas. Como no dataset nenhuma feature possuí esse tipo de distribuição foi aplicado o método de rescaling nas variáveis. Para as features categóricas foi utilizado três diferentes técnicas: a primeira foi o One Hot Encoding, que foi aplicado na feature "state_holiday"; na variável "store_type" foi utilizado o Label Encoding e em "assortment" foi aplicada a técnica de Ordinal Encoding.

Variáveis temporais, por serem ciclicas, necessitam de uma transformação de natureza que dê esse carater ciclico a elas, neste projeto parametrizamos essas váriaveis em componentes de seno e cosseno: $$x_{sin} = sin(x\frac{2\pi}{\tau}), \hspace{1cm} x_{cos} = cos(x\frac{2\pi}{\tau})$$
onde $x$ é a variável original, $x_{sin}$ e $x_{cos}$ a parametrização de $x$ e $\tau$ o período de x, por exemplo, para $x$ = dias $\tau$ = 30.

Além disso, a variável resposta apresenta uma distribuição com uma Skewness positiva, para deixa-la com uma distribuição mais próxima de uma normal (que é uma das premissas para uma melhor performance dos modelos de ML) foi aplicado uma transformação logarítmica do tipo: $y'=ln(1+y)$, onde $y'$ é a variável resposta transformada e $y$ a original.

### 3.5.2 Feature Selection

Agora é necessário selecionar as variáveis que serão mais relevantes para o modelo. A etapa de Análise Exploratória de dados nos dá uma boa intuição das features que devem ser selecionadas, mas podemos buscar uma segunda opinião baseado em como algoritmos de ML performam na inclusão ou exclusão de features. Uma forma de fazer isso de maneira automatizada é utilizando o algoritmo [Boruta](https://github.com/scikit-learn-contrib/boruta_py), que realiza esses teste e nos retorna uma lista de classificação da relevância das features do dataset. Com base nos resultados do Boruta e na EDA selecionamos as variáveis a serem utilizadas nos modelos de ML que serão aplicados a seguir. 

<details><summary><strong> Features selecionadas:</strong> </summary>

- store

- promo

- store_type

- assortment

- competition_distance

- competition_open_since_month

- competition_open_since_year

- promo2

- promo2_since_week

- promo2_since_year

- competition_time_month

- promo_time_week

- month_sin

- month_cos

- day_sin

- day_cos

- day_of_week_sin

- day_of_week_cos

- week_of_year_cos

- week_of_year_sin

</details>

### 3.6 MACHINE LEARNING MODELS

Nesta etapa diferentes modelos de regressão foram treinados, entre eles modelos lineares e não lineares. Inicialmente o modelo foi treinado utilizado. Como métricas de avaliação da performance desses modelos foi utilizados o MAE, MAPE, RMSE e R².

- Mean Absolute Error (MAE): Erro absoluto médio entre os valores reais ($y$) e preditos ($\hat{y}$): $$MAE = \frac{1}{n}\sum_{i=1}^{n}|y_i-\hat{y}_i|$$

- Mean Absolute Percentual Error (MAPE): Erro absoluto médio percentual entre os valores reais e preditos: $$MAPE = \frac{1}{n}\sum_{i=1}^{n}\left|\frac{y_i-\hat{y}_i}{y_i}\right|$$

- Root Mean Squared Error (RMSE): Raiz quadrática do erro quadrático médio e pode variar entre 0 e 1: $$RMSE = \sqrt{\dfrac{1}{n}\sum_{i=1}^{n}(y_i-\hat{y}_i)^2}$$

- R squared (R²): Representa o quão bem a variável resposta é descrita pelas features: $$R^2 = 1 - \frac{\sum_{i=1}^{n}(y_i-\hat{y}_i)^2}{\sum_{i=1}^{n}(y_i-\bar{y}_i)^2}$$

Foram treinados quatro modelos, dois lineares: Linear Regression (LR) e LASSO; e dois não lineares: Random Forest Regressor (RFR) e XGBoost Regressor (XGB). Abaixo as métricas de performance desses modelos:

|Model Name|  MAE  | MAPE (%)|  RMSE  | R² (%) |
|----------|-------|---------|--------|--------|
|   RFR	   | 683.5 |    10   | 1019.2 |   89   |
|   XGB    | 868.9 |    13   | 1238.5 |   83   |
|   LR     | 1867.1|    29   | 2671.0 |   23   |
|   LASSO  | 2198.6|    34   | 3110.5 |  -04.  |

Os modelos lineares apresentaram menor desempenho (RMSE alto e R² baixo) quando comparado com os modelos não lineares, indicando que os dados não podem ser bem descritos por métodos lineares, indicando um nível considerável de complexidade do dataset. Para ter certeza que esses valores de performance não são consequência da escolha da base de treino e teste foi aplicado a técnica de Cross-Validation (CV). 

Essa técnica reserva a base de teste e separa a base de treino em uma nova base de treino e uma outra de validação. Então aplica-se o modelo na base de teste e o valida com a base de validação, depois aleatoriamente defini-se uma nova base de treino e validação e repete-se o processo um número finito de vezes, no final toma-se a média de todas as métricas de performance para avaliar o modelo. 

Neste projeto em questão, como o dataset possuí uma dependência temporal a escolha de novas bases de treino e validação não pode ser aleatória, mas seguindo o seguinte esquema: 

IMAGEM CROSS VALIDATION

Aplicando este método obtemos as seguintes novas métricas de performance para os modelos:

|Model Name|         MAE        |  MAPE (%) |       RMSE       |   R² (%)   |
|----------|--------------------|-----------|------------------|------------|
|   RFR	   |   837.1 +/- 217.71 | 12 +/- 2  | 1256.4 +/- 319.0 |  84 +/- 05 |
|   XGB    | 1076.27 +/- 199.96 | 15 +/- 2  | 1541.7 +/- 278.4 |  76 +/- 03 |
|   LR     | 2081.73 +/- 295.63 | 30 +/- 2  | 2952.5 +/- 468.4 |  14 +/- 07 |
|   LASSO  | 2388.68 +/- 398.48 | 34 +/- 1  | 3369.4 +/- 567.5 | -12 +/- 11 |

Agora podemos confirmar com mais certeza que métodos lineares não conseguem descrever bem a complexidade do dataset. Dos métodos não lineares o que tem melhor performance é o Random Forest Regressor, entretanto o XGBoost apresenta desempenho similar e um tempo de processamento computacional bem menor que o RFR, por conta disso prosseguiremos com ele.

### 3.6.1 Hyperparameter Fine Tunning

Após ter escolhido o modelo agora é  necessário refina-lo para obter uma performance ainda melhor. Existem diferentes formas de fazer isso, neste projeto foi utilizado a Random Search em que, aleatoriamente, altera-se os parâmetros modelo e utiliza-se aqueles que apresentam a melhor performance.

## 3.7 Interpretação e tradução do erro

Nesse ponto temos o modelo já treinado e podemos verificar a performance em cima da base de validação. Além disso os resultados também são traduzidos para o mundo de negócio, ou seja, tradução dos resultados em termos financeiros.

## 3.8 Deploy do modelo

Com o modelo treinado, apresentando uma performance satisfatória e tendo uma compreensão dos resultados em termos de negócio resta coloca-lo em produção.
Para isso foi utilizado um serviço gratuito na plataforma [Render](https://render.com/) para criar uma API capaz de ser acessada por qualquer serviço online. 

Para facilitar o acesso à essa API foi utilizado a API do TelegramBot (API - Rossmann) para criar uma interface (um bot no telegram) que se comunica com a API Render e torna possível que o usuário possa consultar predições das vendas de lojas de maneira simples e remota, sendo necessário apenas uma conexão de internet. Abaixo está representado a arquitetura do deploy.

IMAGEM ESQUEMA DEPLOY

## 4.0 PRINCIPAIS INSIGHTS

## 5.0 PERFORMANCE DO MODELO DE MACHINE LEARNING

## 6.0 PRODUTO FINAL: BOT NO TELEGRAM

## 7.0 CONCLUSÕES 

## 8.0 PRÓXIMOS PASSOS