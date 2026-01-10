main :: IO()
main = do 
  n <- readLn :: IO [Int]
  print(maioremenor n)

maioremenor (x:xs) = helper xs x x

helper [] big less = (big, less)
helper (x:xs) big less 
  | x > big = helper xs x less 
  | x < less = helper xs big x 
  | otherwise = helper xs big less
