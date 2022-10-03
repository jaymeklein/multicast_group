# Leilao
Sistema de leilão baseado num grupo multicast.


<ul>
  <li>O servidor TCP e UDP deverão ser executados em threads separadas simultaneamente.</li>
  <li>Recomendado utilizar interface gráfica ou um framework web para não ter que tratar as strings dos lances.</li>
  <li>Um par de chaves deve ser gerado para <strong>CADA</strong> cliente do leilão.</li>
  <li>Os clientes previamente já terão acesso ao seu respectivo par de chaves.</li>
  <li>* Ideia de fazer com que o servidor (UDP) faça a leitura de uma pasta em busca de um arquivo json com o item do leilão.</li>
</ul>
