# Leilao
Sistema de leilão baseado num grupo multicast.


<h2>Dúvidas / Implementações necessárias</h2>
<ul>
    <li>O servidor TCP e UDP deverão ser executados em threads separadas simultaneamente.</li>
    <li>Thread TCP tratará exclusivamente dos joins dos clientes.</li>
    <li>Thread UDP (Grupo multicast) tratará somente do leilão / dos lances.</li>
    <li>Recomendado utilizar interface gráfica ou um framework web para não ter que tratar as strings dos lances.</li>
    <li>Um par de chaves deve ser gerado para <strong>CADA</strong> cliente do leilão.</li>
    <li>Os clientes previamente já terão acesso ao seu respectivo par de chaves.</li>
    <li>* Ideia de fazer com que o servidor (UDP) faça a leitura de uma pasta em busca de um arquivo json com o item do leilão.</li>
    <li>Servidor indicará o final do leilão de um item, junto com seu ganhador.</li>
    <li>Verificar se o atual cliente tentando conectar já está previamente cadastrado.</li>
    <li>Os clientes criam os pares de chaves publi / priv.</li>
    <li>Servidor define a chave simétrica.</li>
    <li>NÂO deve ser gerado o par de chaves quando o cliente der o Join.</li>
    <li>O servidor deverá verificar se o certificado do cliente já estava cadastrado.</li>
    <li>O parâmetro que o cliente passará vai ser também a chave pública deste cliente.</li>
    <li>O servidor terá a lista de chaves públicas dos clientes e verificará se a chave pública enviada pelo cliente já estava previamente cadastrada.</li>
    <li>Servidor responderá com o endereço do grupo multicast e a chave simétrica (??)</li>
    <li>Cliente terá a chave simétrica e o endereço do grupo multicast.</li>
    <li>cada cliente terá seu par de chaves publicas / privadas.</li>
    <li>cliente enviará em texco claro a sua chave pública ao realizar o join.</li>
    <li>O server udp possui a chave simétrica somente para criptografar as mensagens enviadas ao grupo multicast.<br>EQUANTO o cliente também possui essa chave para decriptografar as mensagens enviadas, (essa chave <strong>simétrica</strong>n ão tem correlação com o par de chaves publi/priv geradas pelo cliente.)</li>
    <li>Servidor responderá a solicitação com a mensagem criptografada com a chave PÚBLICA enviada no passo anterior, com a chave simétrica e o endereço do grupo multicast.</li>
    <li>O cliente irá decriptografar a chave simétrica enviada pelo servidor com sua própria chave privada. (dá pra fazer isso?)</li>
    <li>Caso a chave pública que o cliente enviou não esteja na lista do servidor, o join não ser</li>
    <li>Após o Join o cliente irá receber as mensagens criptografadas pelo servidor.</li>
    <ul>
        <li>Deverá decriptografar as mensagens com a chave simétrica que o servidor enviou previamente.</li>
        <li></li>
    </ul>
</ul>

<ul>
    <li>https://stackoverflow.com/questions/41385014/multithreading-to-run-udp-client-and-udp-server-in-the-same-program</li>
    <li>https://ankush-chavan.medium.com/client-server-messaging-program-using-socket-programming-and-udp-protocol-in-python-fce4d50b47bc</li>
</ul>
