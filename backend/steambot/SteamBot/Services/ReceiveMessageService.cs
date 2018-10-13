using SteamKit2;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;

namespace SteamBot.Services
{
    public class ReceiveMessageService
    {
        SteamClient _steamClient;
        CallbackManager _manager;

        SteamUser _steamUser;
        SteamFriends _steamFriends;

        private string _user = "hacktestbot";//args[ 0 ];
        private string _pass = "GiveMeYourMoney3000";//args[ 1 ];

        private bool _isRunning = false;

        private static readonly HttpClient client = new HttpClient();

        public ReceiveMessageService(string user, string pass)
        {
            _user = user;
            _pass = pass;
        }

        public void Start()
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
            _manager.Subscribe<SteamFriends.PersonaStateCallback>(OnPersonaState);
            _manager.Subscribe<SteamFriends.FriendMsgCallback>(OnMessageReceivedAsync);

            Console.WriteLine("Connecting to Steam...");

            _isRunning = true;

            // initiate the connection
            _steamClient.Connect();

            // create our callback handling loop
            while (_isRunning)
            {
                // in order for the callbacks to get routed, they need to be handled by the _manager
                _manager.RunWaitAllCallbacks(TimeSpan.FromSeconds(5));
            }
        }

        public void Stop()
        {
            _isRunning = false;
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
            //callback.AccountFlags
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

        async void OnMessageReceivedAsync(SteamFriends.FriendMsgCallback callback)
        {
            var values = new Dictionary<string, string>
                {
                    { "sender", _steamFriends.GetFriendPersonaName(callback.Sender).ToString() },
                    { "message", callback.Message },
                    { "profile_url", "https://steamcommunity.com/profiles/"+callback.Sender.ConvertToUInt64() }
                };

            var content = new FormUrlEncodedContent(values);

            var response = await client.PostAsync("https://pivasbot.appspot.com/api/receiveMessage", content);

            var responseString = await response.Content.ReadAsStringAsync();
        }
    }
}
