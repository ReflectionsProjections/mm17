{-# LANGUAGE OverloadedStrings, RecordWildCards, ViewPatterns #-}
import MM17.Client
import System.Environment
import Data.Text(pack)

main = do
  [name, auth] <- fmap (map pack) getArgs
  APICalls{..} <- mkCalls 7000 name auth
  game_join >>= print
  game_turn_get >>= print
  game_info >>= print
  Right (gia@(GameInfoAll _ _ turn objs)) <- game_info_all
  print gia

  let mine = [ix | o@(Ship _ _ _ ix@(ObjectId _) owner _ _) <- objs, owner == name]
  game_turn_post turn (Prelude.concat [[ShipCommand ix (Thrust 20 20), ShipCommand ix (Fire 0)]
                      | ix <- mine]) >>= print
