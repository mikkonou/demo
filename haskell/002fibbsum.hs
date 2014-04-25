import Data.List
fibs = 0 : scanl (+) 1 fibs
fibsum = sum $ filter even $ takeWhile (<4000000) fibs