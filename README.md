===> multitime results
1: poetry run python naive.py
            Mean        Std.Dev.    Min         Median      Max
real        138.586     3.114       133.686     140.614     141.579     
user        133.203     2.603       129.075     133.822     136.283     
sys         2.691       0.177       2.514       2.583       2.953       
===> multitime results
1: poetry run python serial_read.py
            Mean        Std.Dev.    Min         Median      Max
real        35.818      0.632       34.848      36.241      36.462      
user        160.009     1.626       158.174     159.800     162.435     
sys         15.077      0.504       14.367      15.242      15.765      
===> multitime results
1: poetry run python parallel_read.py
            Mean        Std.Dev.    Min         Median      Max
real        29.822      0.770       28.976      29.667      31.151      
user        159.936     1.804       158.236     158.893     162.358     
sys         9.032       0.362       8.543       9.017       9.653       
===> multitime results
1: poetry run python parallel_read_write.py
            Mean        Std.Dev.    Min         Median      Max
real        17.747      0.344       17.221      17.927      18.125      
user        152.405     0.672       151.822     151.888     153.283     
sys         4.163       0.111       3.948       4.226       4.241       
===> multitime results
1: poetry run python parallel_read_write_at_once.py
            Mean        Std.Dev.    Min         Median      Max
real        18.628      1.057       17.366      18.556      20.457      
user        146.779     1.893       143.956     146.676     149.248     
sys         4.340       0.124       4.182       4.277       4.499   