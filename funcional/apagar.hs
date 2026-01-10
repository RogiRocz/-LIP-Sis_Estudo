main :: IO()
main = do 
  array <- readLn :: IO [Int]
  n <- readLn :: IO Int
  print(apagar array n)

apagar :: [Int] -> Int -> [Int]
apagar [] n = []
apagar (x:xs) n 
  | x == n = apagar xs n 
  | otherwise = x:apagar xs n
