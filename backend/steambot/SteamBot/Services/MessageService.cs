using SteamKit2;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;

namespace SteamBot.Services
{
    public enum Command
    {
        SendSingle,
        SendAll,
        AcceptFriends,
        GetInfo,
        GetAllIds,
        GetFriendInfo
    }
    public class MessageService
    {
        SteamClient _steamClient;
        CallbackManager _manager;

        SteamUser _steamUser;
        SteamFriends _steamFriends;

        private string _user = "hacktestbot";//args[ 0 ];
        private string _pass = "GiveMeYourMoney3000";//args[ 1 ];

        private string _messageText;

        private bool _isRunning = false;
        private bool _isMessageSent = false;

        private string _userId = null;

        Command _cmd;

        public MessageService() : this("This is default message sent from chat bot: Zdarowa")
        {
        }

        public MessageService(string messageText)
        {
            _messageText = messageText;
        }

        public bool SendSingle(string userId)
        {
            _userId = userId;
            _cmd = Command.SendSingle;
            var result = RunClient();
            return result;
        }

        public bool SendAllFriends()
        {
            _cmd = Command.SendAll;
            var result = RunClient();
            return result;
        }

        public bool AcceptFriendsAndSendMessage()
        {
            _cmd = Command.AcceptFriends;
            var result = RunClient();
            return result;
        }

        private UserInfoVm _userInfoVm;
        public UserInfoVm GetBotInfo()
        {
            _cmd = Command.GetInfo;
            _userInfoVm = new UserInfoVm();
            var result = RunClient();
            return _userInfoVm;
        }

        private FriendInfoVm _friendInfoVm;
        public FriendInfoVm GetFriendInfo(string userId)
        {
            _userId = userId;
            _cmd = Command.GetFriendInfo;
            _friendInfoVm = new FriendInfoVm();
            var result = RunClient();
            return _friendInfoVm;
        }

        List<string> _friendsIds;
        public IEnumerable<string> GetAllIds()
        {
            _friendsIds = new List<string>();
            _cmd = Command.GetAllIds;
            var result = RunClient();
            return _friendsIds.Distinct();
        }

        private bool RunClient()
        {
            // create our steamclient instance
            var configuration = SteamConfiguration.Create(b => b.WithProtocolTypes(ProtocolTypes.Tcp));
            _steamClient = new SteamClient(configuration);
            // create the callback _manager which will route callbacks to function calls
            _manager = new CallbackManager(_steamClient);

            // get the steamuser handler, which is used for logging on after successfully connecting
            _steamUser = _steamClient.GetHandler<SteamUser>();
            // get the steam friends handler, which is used for interacting with friends on the network after logging on
            _steamFriends = _steamClient.GetHandler<SteamFriends>();

            // register a few callbacks we're interested in
            // these are registered upon creation to a callback _manager, which will then route the callbacks
            // to the functions specified
            _manager.Subscribe<SteamClient.ConnectedCallback>(OnConnected);
            _manager.Subscribe<SteamClient.DisconnectedCallback>(OnDisconnected);

            _manager.Subscribe<SteamUser.LoggedOnCallback>(OnLoggedOn);
            _manager.Subscribe<SteamUser.LoggedOffCallback>(OnLoggedOff);

            // we use the following callbacks for friends related activities
            _manager.Subscribe<SteamUser.AccountInfoCallback>(OnAccountInfo);
            _manager.Subscribe<SteamFriends.FriendsListCallback>(OnFriendsList);
            _manager.Subscribe<SteamFriends.PersonaStateCallback>(OnPersonaState);
            _manager.Subscribe<SteamFriends.FriendAddedCallback>(OnFriendAdded);

            Console.WriteLine("Connecting to Steam...");

            _isRunning = true;

            // initiate the connection
            _steamClient.Connect();

            Thread.Sleep(500);

            // create our callback handling loop
            int attempts = 5;
            while (_isRunning && attempts > 0 && !_isMessageSent)
            {
                // in order for the callbacks to get routed, they need to be handled by the _manager
                _manager.RunWaitAllCallbacks(TimeSpan.FromSeconds(5));
                attempts--;
            }

            return _isMessageSent;
        }

        void OnConnected(SteamClient.ConnectedCallback callback)
        {
            Console.WriteLine("Connected to Steam! Logging in '{0}'...", _user);

            _steamUser.LogOn(new SteamUser.LogOnDetails
            {
                Username = _user,
                Password = _pass,
            });
        }

        void OnDisconnected(SteamClient.DisconnectedCallback callback)
        {
            Console.WriteLine("Disconnected from Steam");
        }

        void OnLoggedOn(SteamUser.LoggedOnCallback callback)
        {
            if (callback.Result != EResult.OK)
            {
                if (callback.Result == EResult.AccountLogonDenied)
                {
                    // if we recieve AccountLogonDenied or one of it's flavors (AccountLogonDeniedNoMailSent, etc)
                    // then the account we're logging into is SteamGuard protected
                    // see sample 5 for how SteamGuard can be handled

                    Console.WriteLine("Unable to logon to Steam: This account is SteamGuard protected.");

                    _isRunning = false;
                    return;
                }

                Console.WriteLine("Unable to logon to Steam: {0} / {1}", callback.Result, callback.ExtendedResult);

                _isRunning = false;
                return;
            }

            Console.WriteLine("Successfully logged on!");

            // at this point, we'd be able to perform actions on Steam

            // for this sample we wait for other callbacks to perform logic
        }

        void OnAccountInfo(SteamUser.AccountInfoCallback callback)
        {
            // before being able to interact with friends, you must wait for the account info callback
            // this callback is posted shortly after a successful logon

            // at this point, we can go online on friends, so lets do that
            _steamFriends.SetPersonaState(EPersonaState.Online);
            if (_cmd == Command.GetInfo)
            {
                _userInfoVm.botName = _steamFriends.GetPersonaName();
                _userInfoVm.botStatus = _steamFriends.GetPersonaState().ToString();
                _userInfoVm.friendsCount = _steamFriends.GetFriendCount();
                _userInfoVm.country = callback.Country;
                _userInfoVm.facebookName = callback.FacebookName;
                _userInfoVm.flags = callback.AccountFlags.ToString();
                _userInfoVm.countAuthComputers = callback.CountAuthedComputers.ToString();
                _userInfoVm.state = _steamFriends.GetPersonaState().ToString();
                _userInfoVm.steamId = _steamUser.SteamID.ToString();
                _userInfoVm.profileUrl = "https://steamcommunity.com/profiles/" + _steamUser.SteamID.ConvertToUInt64().ToString();
                _isMessageSent = true;
            }
        }

        void OnFriendsList(SteamFriends.FriendsListCallback callback)
        {
            // at this point, the client has received it's friends list

            int friendCount = _steamFriends.GetFriendCount();

            Console.WriteLine("We have {0} friends", friendCount);

            for (int x = 0; x < friendCount; x++)
            {
                // steamids identify objects that exist on the steam network, such as friends, as an example
                SteamID steamIdFriend = _steamFriends.GetFriendByIndex(x);
                // we'll just display the STEAM_ rendered version
                Console.WriteLine("Friend: {0}", steamIdFriend.Render());

                if (_cmd == Command.SendAll)
                {
                    _steamFriends.SendChatMessage(steamIdFriend, EChatEntryType.ChatMsg, _messageText);
                    Thread.Sleep(500);
                }
                else if (_cmd == Command.SendSingle)
                {
                    if (_userId == steamIdFriend.ConvertToUInt64().ToString())
                    {
                        _steamFriends.SendChatMessage(steamIdFriend, EChatEntryType.ChatMsg, _messageText);
                        _isMessageSent = true;
                        break;
                    }
                }
                else if (_cmd == Command.AcceptFriends)
                {
                    foreach (var friend in callback.FriendList)
                    {
                        if (friend.Relationship == EFriendRelationship.RequestRecipient)
                        {
                            // this _user has added us, let's add him back and send him a message
                            _steamFriends.AddFriend(friend.SteamID);
                            _steamFriends.SendChatMessage(friend.SteamID, EChatEntryType.ChatMsg, _messageText);
                            _isMessageSent = true;
                        }
                    }
                }
                else if (_cmd == Command.GetAllIds)
                {
                    foreach (var friend in callback.FriendList)
                    {
                        _friendsIds.Add(friend.SteamID.ConvertToUInt64().ToString());
                    }
                    _isMessageSent = true;
                }
                else if (_cmd == Command.GetFriendInfo)
                {
                    if (_userId == steamIdFriend.ConvertToUInt64().ToString())
                    {
                        var val = _steamFriends.RequestProfileInfo(steamIdFriend).ToTask().Result;
                        _friendInfoVm.country = val.CountryName;
                        _friendInfoVm.summary = val.Summary;
                        _friendInfoVm.realName = val.RealName;
                        _friendInfoVm.headline = val.Headline;
                        _friendInfoVm.state = val.StateName;
                        _friendInfoVm.steamId = steamIdFriend.ToString();
                        _friendInfoVm.profileUrl = "https://steamcommunity.com/profiles/" + steamIdFriend.ConvertToUInt64().ToString();
                        _isMessageSent = true;
                    }
                }
            }
            if (_cmd == Command.SendAll)
            {
                _isMessageSent = true;
            }
        }

        void OnFriendAdded(SteamFriends.FriendAddedCallback callback)
        {
            // someone accepted our friend request, or we accepted one
            Console.WriteLine("{0} is now a friend", callback.PersonaName);
        }

        void OnPersonaState(SteamFriends.PersonaStateCallback callback)
        {
            // this callback is received when the persona state (friend information) of a friend changes
            // for this sample we'll simply display the names of the friends
            Console.WriteLine("State change: {0}", callback.Name);
        }

        void OnLoggedOff(SteamUser.LoggedOffCallback callback)
        {
            Console.WriteLine("Logged off of Steam: {0}", callback.Result);
        }
    }
}
