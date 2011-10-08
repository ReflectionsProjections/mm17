{-# LANGUAGE OverloadedStrings, RecordWildCards, ViewPatterns, GeneralizedNewtypeDeriving #-}
module MM17.Client where
import Control.Applicative
import Control.Exception
import System.Environment
import Data.Map(size)
import Data.Text
import Data.Aeson as A
import Data.Aeson.Types as A
import Data.Vector hiding ((++))
import Network.HTTP.Enumerator(Request(..))
import Network.HTTP.Enumerator
import Network.HTTP.Types
import qualified Data.Text.Encoding as E
import Control.Monad.IO.Class
import Data.Attoparsec.Enumerator
import Data.Enumerator
import Data.Enumerator.Text(consume)
import qualified Data.ByteString as S hiding (pack)
import qualified Data.ByteString.Char8 as S
import qualified Data.ByteString.Lazy as L

-- import Data.Attoparsec(parseOnly)

type APICall m a = m (Either Value a)
data APICalls m = APICalls {
  game_info :: APICall m GameInfo,
  game_info_all :: APICall m GameInfoAll,
  game_turn_get :: APICall m TurnResponse,
  game_join :: APICall m JoinResponse,
  game_turn_post :: Int -> [Command] -> APICall m Value
  }

mkCalls :: (MonadIO m) => Int -> Text -> Text -> m (APICalls m)
mkCalls port (E.encodeUtf8 -> name) tauth@(E.encodeUtf8 -> auth) = do
  manager <- liftIO newManager
  let doReq :: (FromJSON r, MonadIO m) => Request m -> APICall m r
      doReq req = run_ $ http req (\s _ -> if s == statusOK
         then do v <- iterParser json
                 case fromJSON v of
                   Success r -> return (Right r)
                   A.Error msg -> throwError (ErrorCall msg)
         else fmap Left (iterParser json)) manager
      base = def {method = methodGet,
                  host = "127.0.0.1",
                  port = port}
      game_info =     doReq $ base { path = "/game/info" }
      game_info_all = doReq $ base { path = "/game/info/all",
                                       queryString = [("auth",Just auth)] }
      game_turn_get =   doReq $ base { path = "/game/turn" }
      game_join =       doReq $ base { path = "/game/join",
                                       queryString = [("name",Just name),
                                                      ("auth",Just auth)] }
      game_turn_post turn commands = doReq $ base { method = methodPost,
                                                    path = S.append "/game/turn/" (S.pack (show turn)), 
                                                    requestBody = RequestBodyLBS (encode (encodeTurn tauth commands)) }
  return APICalls{..}

-- GET requests use query args for auth and name.
-- POST body is single json string, with fields for name, auth, etc.

{- request format
{"auth":<auth>,
"actions":[<actions>]}
common action format -
{"obj_type":"ship",
"command":<cmd>,
"obj_id":<ship_id>,
"args":<params>}
thrust -
  <cmd> = "thrust"
  <params> = {"accel":[<dx>,<dy>]}
fire -
  <cmd> = "fire"
  <params> = {"angle":<angle>}
 -}
data ShipOrder = Thrust Double Double
               | Fire Double
               | Scan ObjectId -- ^ target of scan
               | CreateRefinery ObjectId -- ^ asteroid to build on
               | CreateBase ObjectId -- ^ planet to build on
data BaseOrder = CreateShip Position
               | SalvageShip ObjectId -- ^ target ship
               | RepairShip ObjectId -- ^ target ship
               | BaseDestroy -- ^ Why?
data RefineryOrder = RefineryDestroy -- ^ Why?
data PlayerOrder = Forfeit
data Command = ShipCommand ObjectId ShipOrder
             | BaseCommand ObjectId BaseOrder
             | RefineryCommand ObjectId RefineryOrder
             | PlayerCommand PlayerOrder
instance ToJSON Command where
  toJSON (ShipCommand (ObjectId ship_id) order) = 
    let cmd cmd_name args =
          object ["obj_type" .= String "ship",
                  "obj_id" .= ship_id,
                  "command" .= String cmd_name,
                  "args" .= object args]
    in case order of
      Fire angle -> cmd "fire" ["angle" .= angle]
      Thrust ax ay -> cmd "thrust" ["accel" .= (ax,ay)]
      Scan target -> cmd "scan" ["scan_id" .= target]
      CreateRefinery asteroid -> cmd "create_refinery" ["asteroid" .= asteroid]
      CreateBase planet -> cmd "create_base" ["planet" .= planet]
  toJSON (BaseCommand (ObjectId base_id) order) = 
    let cmd cmd_name args =
          object ["obj_type" .= String "base",
                  "obj_id" .= base_id,
                  "command" .= String cmd_name,
                  "args" .= object args]
    in case order of
      CreateShip position -> cmd "create_ship" ["position" .= position]
      SalvageShip ship -> cmd "salvage_ship" ["ship_id" .= ship]
      RepairShip ship -> cmd "repair_ship" ["ship_id" .= ship]
      BaseDestroy -> cmd "destroy" []
  toJSON (RefineryCommand (ObjectId refinery_id) order) = 
    let cmd cmd_name args =
          object ["obj_type" .= String "refinery",
                  "obj_id" .= refinery_id,
                  "command" .= String cmd_name,
                  "args" .= object args]
    in case order of
      RefineryDestroy -> cmd "destroy" []
  toJSON (PlayerCommand Forfeit) = 
    object ["obj_type" .= String "player",
            "command" .= String "forfeit"]

encodeTurn :: Text -> [Command] -> Value
encodeTurn auth orders = object ["auth" .= auth, "actions" .= orders]

{- response formats 
joining
{"success":<bool>,"message":<str>}
-}
data JoinResponse = JoinResponse Bool Text
  deriving (Show)
instance FromJSON JoinResponse where
  parseJSON (Object o) = JoinResponse <$> o .: "success" <*> o .: "message"
  parseJSON _ = fail "/game/join response expected to be object"
{- turn response
{"turn":<number>}
-}
data TurnResponse = TurnResponse Integer
  deriving (Show)
instance FromJSON TurnResponse where
  parseJSON (Object o) = TurnResponse <$> o .: "turn"
  parseJSON _ = fail "/game/turn resonse expected to be object"
{- game info
{"active_players":[<name>],"game_active":<bool>,"turn":<num>
-}
data GameInfo = GameInfo [Text] Bool Int
  deriving (Show)
instance FromJSON GameInfo where
  parseJSON (Object o) = GameInfo <$> o .: "active_players" <*> o .: "game_active" <*> o .: "turn"
  parseJSON _ = fail "/game/info response expected to be object"
data GameInfoAll = GameInfoAll [Text] Bool Int [GameObject]
  deriving (Show)
instance FromJSON GameInfoAll where
  parseJSON (Object o) = GameInfoAll <$> o.: "alive_players" <*> o .: "game_active" <*> o .: "turn" <*> o .: "objects"
   <|> error (show o)
  parseJSON _ = fail "/game/info/all response expected to be object"

newtype Alive = Alive Bool
  deriving (Show, ToJSON, FromJSON)
newtype Direction = Direction Double
  deriving (Show, ToJSON, FromJSON)
newtype Health = Health Int
  deriving (Show, ToJSON, FromJSON)
newtype ObjectId = ObjectId Integer
  deriving (Show, ToJSON, FromJSON)
newtype Position = Position (Double,Double)           
  deriving (Show, ToJSON, FromJSON)
newtype Velocity = Velocity (Double,Double)           
  deriving (Show, ToJSON, FromJSON)

data GameObject = Ship Alive Direction Health ObjectId Text Position Velocity
  deriving (Show)
                  
instance FromJSON GameObject where
  parseJSON (Object o) = do
    String "ship" <- o .: "type"
    Ship <$> o .: "alive" <*> o .: "direction" <*> o .: "health" <*> o .: "id" <*> o .: "owner" <*> o .: "position" <*> o .: "velocity"
  parseJSON _ = fail "game object expected to be object"
