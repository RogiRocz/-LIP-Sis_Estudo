main :: IO()
main = do 
  array <- readLn :: IO [Int]
  print(produto array)

produto [] = 1
produto (x:xs) = x * produto xs
