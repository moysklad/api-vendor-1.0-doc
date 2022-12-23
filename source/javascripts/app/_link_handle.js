//все, что ведет на НЕ https://dev.moysklad.ru/doc/api/vendor) в документации открываются в новой вкладке
$(function () {
  'use strict';
  var url = `${window.location.hostname}/doc/api/vendor`;
  $(`a:not([href^="http://${url}"], [href^="https://${url}"], [href^='#'], [href^='/#'])`).attr("target", "_blank");
  $('a[href=""]').removeAttr("target");
})
