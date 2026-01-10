main :: IO()
main = do 
  n <- readLn :: IO [Int]
  print(maior n)

maior :: [Int] -> (Int, Int)
maior arr = (max, findItem max arr 0)
  where
    max = findMax arr (head arr)

findMax :: [Int] -> Int -> Int
findMax [] n = n
findMax (x : xs) n
  | x > n = findMax xs x
  | otherwise = findMax xs n

findItem :: Int -> [Int] -> Int -> Int
findItem n [] i = -1
findItem n (x : xs) i
  | n == x = i
  | otherwise = findItem n xs (i + 1)
