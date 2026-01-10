main :: IO()
main = do 
  n <- readLn :: IO Int
  print(fatorial n)

fatorial n
  | n <= 0 = 1
  | otherwise = n * fatorial (n - 2)
