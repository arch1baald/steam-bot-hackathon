using Microsoft.AspNetCore.Cors;
using Microsoft.AspNetCore.Mvc;
using SteamBot.Services;

namespace SteamBot.Controllers
{
    [EnableCors("CorsPolicy")]
    [Route("api/bot")]
    [ApiController]
    public class BotController : ControllerBase
    {
        [HttpPost("/sendsingle")]
        public ActionResult<string> SendOne(string user64Id, string messageText)
        {
            var service = new MessageService(messageText);
            var isSent = service.SendSingle(user64Id);
            return Ok(isSent);
        }

        [HttpPost("/sendall")]
        public IActionResult SendAll(string messageText)
        {
            var service = new MessageService(messageText);
            var isSent = service.SendAllFriends();
            return Ok(isSent);
        }

        [HttpGet("/getfriendsIds")]
        public IActionResult GetAllIds()
        {
            var service = new MessageService();
            var result = service.GetAllIds();
            return Ok(result);
        }

        [HttpPost("/acceptFriendsAndSendMessage")]
        public IActionResult AcceptFriendsRequestsAndSendMessage(string messageText)
        {
            var service = new MessageService(messageText);
            var isSent = service.AcceptFriendsAndSendMessage();
            return Ok(isSent); // If false, no pending friends requests.
        }

        [HttpPost("/userInfo")]
        public IActionResult GetUserInfo()
        {
            var service = new MessageService();
            var userInfo = service.GetBotInfo();
            return Ok(userInfo);
        }

        ReceiveMessageService receiver = new ReceiveMessageService();
        [HttpPost("/runmessagesreceiver")]
        public IActionResult RunMessagesReceiver()
        {
            receiver.Start();
            return Ok();
        }

        [HttpPost("/stopmessagesreceiver")]
        public IActionResult StopMessagesReceiver()
        {
            receiver.Stop();
            return Ok();
        }
    }
}
