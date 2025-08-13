jupyter_py311\Scripts\activate
jupyter notebook

sklearn

# =============================================================================
# Imports e dependências
# =============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Pré-processamento
from sklearn.preprocessing import MinMaxScaler

# Clusterização Hierárquica
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster

# Clusterização K-Means
from sklearn.cluster import KMeans

# Métrica de qualidade de clusters
from sklearn.metrics import silhouette_score

# =============================================================================
# 1. Leitura e preparação inicial dos dados
# =============================================================================
# 1.1. Carrega o CSV com dados de propensão de revenda
tabela = pd.read_csv('/content/drive/MyDrive/FIA/propensao_revenda_abt.csv')

# 1.2. Filtra apenas a safra de referência '2018-03-01'
tabela_safra = tabela.loc[
    tabela['data_ref_safra'] == '2018-03-01',
    ['tot_orders_12m','tot_items_12m','tot_items_dist_12m','receita_12m','recencia']
]

# 1.3. Exibe as primeiras linhas para checagem rápida
print("Amostra dos dados filtrados:\n", tabela_safra.head(), "\n")

# =============================================================================
# 2. Escalonamento (Min-Max Scaling)
# =============================================================================
# Motivação: muitas técnicas de clusterização são sensíveis à escala das variáveis.
# O MinMaxScaler normaliza cada feature para o intervalo [0,1], preservando
# a forma da distribuição original, mas garantindo comparabilidade.
escalador = MinMaxScaler()
X = escalador.fit_transform(tabela_safra.values)

# Visualiza os primeiros registros escalonados
print("Primeiros 5 registros após escalonamento:\n", X[:5], "\n")


# =============================================================================
# 3. Clusterização Hierárquica (Ward linkage)
# =============================================================================
# 3.1. Cálculo do linkage com método de Ward:
#      - busca minimizar a soma das variâncias dentro de cada cluster.
#      - retorna uma matriz de fusões (cluster a cluster).
h_cluster = linkage(X, method='ward')

# 3.2. Plot do dendrograma para visualizar a fusão de clusters em diferentes
#      níveis de distância. Útil para escolher um possível número de clusters.
plt.figure(figsize=(10, 5))
dendrogram(h_cluster, truncate_mode='level', p=5)  # mostra apenas os 5 primeiros níveis
plt.title('Dendrograma - Clusterização Hierárquica (Ward)')
plt.xlabel('Amostras ou clusters iniciais')
plt.ylabel('Distância de fusão')
plt.show()

# 3.3. Corte do dendrograma para obter exatamente k clusters:
k_hier = 4
labels_hier = fcluster(h_cluster, k_hier, criterion='maxclust')

# 3.4. Avaliação da qualidade dos clusters hierárquicos:
#      a) Silhueta: mede coesão e separação (valor em [-1,1], quanto mais perto de 1, melhor)
sil_score_hier = silhouette_score(X, labels_hier)
#      b) Inércia manual: soma das distâncias quadráticas de cada ponto ao centróide do seu cluster
inertia_hier = 0
for cl in np.unique(labels_hier):
    centroid = X[labels_hier == cl].mean(axis=0)
    inertia_hier += ((X[labels_hier == cl] - centroid) ** 2).sum()

print(f"Hierárquica k={k_hier} → Silhueta: {sil_score_hier:.3f}, Inércia: {inertia_hier:.3f}\n")


# =============================================================================
# 4. Clusterização K-Means
# =============================================================================
# 4.1. Teste de vários valores de k para avaliar inércia e silhueta
ks = range(2, 11)
inertias = []
silhouettes = []

for k in ks:
    km = KMeans(n_clusters=k, random_state=42)
    km_labels = km.fit_predict(X)
    inertias.append(km.inertia_)                        # atributo inertia_ do KMeans
    silhouettes.append(silhouette_score(X, km_labels))  # silhueta para cada k

# 4.2. Plot do Método do Cotovelo (Inércia vs k)
plt.figure(figsize=(8, 4))
plt.plot(ks, inertias, 'o-', color='C0')
plt.title('Elbow Method (K-Means)')
plt.xlabel('Número de clusters k')
plt.ylabel('Inércia (Soma de distâncias quadráticas)')
plt.show()

# 4.3. Plot dos Scores de Silhueta (Silhueta vs k)
plt.figure(figsize=(8, 4))
plt.plot(ks, silhouettes, 'o-', color='C1')
plt.title('Silhouette Score (K-Means)')
plt.xlabel('Número de clusters k')
plt.ylabel('Silhouette Score')
plt.show()

# 4.4. Seleção automática do k que maximiza o Silhouette Score
k_opt = ks[np.argmax(silhouettes)]
print(f"k ótimo pelo Silhouette Score: {k_opt}")

# 4.5. Ajuste final do modelo K-Means com o k ótimo
km_opt = KMeans(n_clusters=k_opt, random_state=42)
labels_km = km_opt.fit_predict(X)

# 4.6. Métricas para o modelo final
print(f"K-Means k={k_opt} → Inércia: {km_opt.inertia_:.3f}, "
      f"Silhueta: {silhouette_score(X, labels_km):.3f}\n")


# 4.7. Visualização dos clusters em 2D (duas primeiras features escalonadas)
plt.figure(figsize=(6, 6))
plt.scatter(X[:, 0], X[:, 1], c=labels_km, cmap='tab10', s=10)
plt.title(f'Clusters K-Means (k={k_opt})')
plt.xlabel('Feature 1 (escalonada)')
plt.ylabel('Feature 2 (escalonada)')
plt.show()



# =============================================================================
# 5. Análise e comparação dos clusters
# =============================================================================
# 5.1. Anexa rótulos de cluster ao DataFrame original
tabela_safra['cluster_hier'] = labels_hier
tabela_safra['cluster_km']   = labels_km

# 5.2. Estatísticas descritivas para cada cluster Hierárquico
print("=== Estatísticas por cluster (Hierárquica) ===")
print(tabela_safra.groupby('cluster_hier').describe().T, "\n")

# 5.3. Estatísticas descritivas para cada cluster K-Means
print("=== Estatísticas por cluster (K-Means) ===")
print(tabela_safra.groupby('cluster_km').describe().T)

# 5.4. Boxplots comparativos entre Hierárquica e K-Means
# Seleciona as mesmas variáveis numéricas usadas para clusterização
cols = ['tot_orders_12m','tot_items_12m','tot_items_dist_12m','receita_12m','recencia']

# Cria um figure com 2 subplots (um acima do outro)
fig, axes = plt.subplots(2, 1, figsize=(12, 10), sharey=False)

# Boxplot para clusters hierárquicos
tabela_safra.boxplot(
    column=cols,
    by='cluster_hier',
    ax=axes[0],
    grid=False
)
axes[0].set_title('Boxplots por Cluster Hierárquico')
axes[0].set_xlabel('Cluster Hierárquico')
axes[0].set_ylabel('Valor Escalonado')

# Boxplot para clusters K-Means
tabela_safra.boxplot(
    column=cols,
    by='cluster_km',
    ax=axes[1],
    grid=False
)
axes[1].set_title('Boxplots por Cluster K-Means')
axes[1].set_xlabel('Cluster K-Means')
axes[1].set_ylabel('Valor Escalonado')

# Ajusta layout e remove o título automático do agrupamento
plt.suptitle('Comparação de Distribuição das Variáveis por Método de Clusterização', fontsize=14)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()