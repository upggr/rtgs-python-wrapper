var EventSource = require('eventsource');
var es = new EventSource('http://195.201.17.80:8000//accounts/GCQ2WFN74IOHNRCKS5HWQGM73QVOCYRX5VN53FFQREJDHJ7BM5U7PJCH/payments');
es.onmessage = function(message) {
  var result = message.data ? JSON.parse(message.data) : message;
  console.log('New payment:');
  console.log(result);
};
es.onerror = function(error) {
  console.log('An error occured!');
}