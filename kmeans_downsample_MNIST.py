def main():

  filename = 'processed_MNIST/large_files/MNIST_row_labels.txt'
  # filename = 'processed_MNIST/random_subsampling/MNIST_1000x_random_subsample_0.txt'
  df = load_df_using_clustergrammer(filename)

  ds_df, mbk_labels = run_kmeans_mini_batch(df, 100, axis=1)

  # save
  ds_df.to_csv('processed_MNIST/kmeans_downsample/tmp.txt', sep='\t')

def run_kmeans_mini_batch(df, n_clusters, axis=0):
  from sklearn.cluster import MiniBatchKMeans
  import pandas as pd
  import numpy as np

  # downsample rows
  if axis == 0:
    X = df
  else:
    X = df.transpose()
  # kmeans is run with rows as data-points and columns as dimensions
  mbk = MiniBatchKMeans(init='k-means++', n_clusters=n_clusters,
                        max_no_improvement=10, verbose=0)

  # need to loop through each label (each k-means cluster) and count how many
  # points were given this label. This will give the population size of each label
  # For MNIST, I also need to get the digit breakdown of each cluster to see what
  # digits make up each cluster. Then I can work on overrepresentation examples.
  ################################################
  mbk.fit(X)
  mbk_labels = mbk.labels_
  mbk_clusters = mbk.cluster_centers_

  mbk_cluster_names, mbk_cluster_pop = np.unique(mbk_labels, return_counts=True)

  print('============================')
  print('mbk cluster names')
  print(mbk_cluster_names)
  print('mbk cluster populations')
  print(mbk_cluster_pop)
  print('============================')
  print(mbk_labels)

  row_numbers = range(n_clusters)
  row_labels = [ 'cluster-' + str(i) for i in row_numbers]

  # add number of points in each cluster
  cluster_cats = []
  for i in range(n_clusters):

    inst_name = 'cell-clusters: ' + row_labels[i]
    inst_count =  'number of cells: '+ str(mbk_cluster_pop[i])
    inst_tuple = ( inst_name, inst_count )
    cluster_cats.append(inst_tuple)

  print('cluster cats')
  print(len(cluster_cats))
  print(cluster_cats)

  ds = mbk_clusters

  if axis == 0:
    cols = df.columns.tolist()
  else:
    cols = df.index.tolist()


  # ds_df = pd.DataFrame(data=ds, columns = cols, index=cluster_cats)

  # ds_df is always downsampling the rows, if the use wanted to downsample the
  # columns, the df will be switched back later
  ds_df = pd.DataFrame(data=ds, index=cluster_cats, columns=cols)

  # swap back for downsampled columns
  if axis == 1:
    ds_df = ds_df.transpose()

  return ds_df, mbk_labels

def load_df_using_clustergrammer(filename):
  from copy import deepcopy
  from clustergrammer import Network

  net = deepcopy(Network())
  net.load_file(filename)
  tmp_df = net.dat_to_df()
  df = tmp_df['mat']

  return df

main()