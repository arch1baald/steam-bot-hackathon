using Microsoft.AspNetCore.Cors;
using Microsoft.AspNetCore.Mvc;
using SteamBot.Services;
using System;
using System.Threading.Tasks;

namespace SteamBot.Controllers
{
    [EnableCors("CorsPolicy")]
    [Route("api/bot")]
    [ApiController]
    public class BotController : ControllerBase
    {
        [HttpPost("/sendsingle")]
        public ActionResult<string> SendOne(string user, string pass, string user64Id, string messageText)
        {
            var service = new MessageService(user, pass, messageText);
            var isSent = service.SendSingle(user64Id);
            return Ok(isSent);
        }

        [HttpPost("/sendall")]
        public IActionResult SendAll(string user, string pass, string messageText)
        {
            var service = new MessageService(user, pass, messageText);
            var isSent = service.SendAllFriends();
            return Ok(isSent);
        }

        [HttpGet("/getfriendsIds")]
        public IActionResult GetAllIds(string user, string pass)
        {
            var service = new MessageService(user, pass);
            var result = service.GetAllIds();
            return Ok(result);
        }

        [HttpGet("/getbot64Id")]
        public IActionResult GetBot64Id(string user, string pass)
        {
            var service = new MessageService(user, pass);
            var result = service.GetBot64Id();
            return Ok(result);
        }

        [HttpPost("/acceptFriendsAndSendMessage")]
        public IActionResult AcceptFriendsRequestsAndSendMessage(string user, string pass, string messageText)
        {
            var service = new MessageService(user, pass, messageText);
            var isSent = service.AcceptFriendsAndSendMessage();
            return Ok(isSent); // If false, no pending friends requests.
        }

        [HttpPost("/botInfo")]
        public IActionResult GetUserInfo(string user, string pass)
        {
            var service = new MessageService(user, pass);
            var userInfo = service.GetBotInfo();
            return Ok(userInfo);
        }

        [HttpPost("/friendInfo")]
        public IActionResult GetFriendInfo(string user, string pass, string user64Id)
        {
            var service = new MessageService(user, pass);
            var userInfo = service.GetFriendInfo(user64Id);
            return Ok(userInfo);
        }

        ReceiveMessageService receiver;
        [HttpPost("/runmessagesreceiver")]
        public IActionResult RunMessagesReceiver(string user, string pass)
        {
            receiver = new ReceiveMessageService(user, pass);
            var ts = Task.Run((Action) receiver.Start);
            return Ok();
        }

        [HttpPost("/stopmessagesreceiver")]
        public IActionResult StopMessagesReceiver(string user, string pass)
        {
            if (receiver != null)
            {
                receiver.Stop();
            }
            return Ok();
        }
    }
}
