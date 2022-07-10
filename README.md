# PROJETO PADARIA

Esse foi meu segundo projeto do Jovem Programador módulo 2

Esse projeto na verdade é uma evolução natural do projeto da oficina, pois me baseei bastante no projeto da oficina para desenvolver este projeto com inúmeras melhorias e também para que ele ficasse com um nível mais avançado do que o primeiro (projeto da oficina).

Principais evoluções em relação ao projeto da oficina:
- Na parte da interação com o banco de dados, nesta versão da padaria já foi evoluído para evitar risco de SQL injection
- No sistema da padaria foi incluído uma seção apenas para estatísticas dos dados
- Como a maioria dos registros do banco de dados se relaciona de alguma forma, incluí o campo de status, onde sinaliza se o registro está ativo ou inativo, dessa forma mantendo os registros e integridade do banco de dados

O projeto consiste basicamente em:
- Um cadastro de usuários (somente permitido a usuários com permissão ROOT)
- Permissão de acessos dependendo do nível do usuário
- Cadastro simples de clientes
- Cadastro de funcionários
- Cadastro de produtos
- Registro de vendas (simula emissão de uma nota fiscal)
- Estatísticas dos dados

É utilizado o banco de dados Sqlite3.

Regra de negócio deste projeto:

O usuário deve ser cadastrado apenas pelo ROOT ou por algum usuário com permissões de ROOT, este por sua vez poderá, no momento do cadastro, ou a qualquer momento, setar as permissões dos demais usuários, incluindo dar a eles permissão de ROOT, as permissões possíveis são:

- Somente consulta
- Criar (permite cadastrar novos produtos, clientes e emitir notas)
- Editar (permite alterar produtos, clientes e notas pendentes)
- Excluir (permite desativar produtos e clientes e cancelar notas)
- ROOT (permite setar permissões para os usuários, e também cadastrar, editar ou desligar funcionários)

OBS: Um usuário pode acumular várias permissões de acordo com o que for setado pelo ROOT.

Assim como no projeto da oficina, existe um superusuário que através dele poderá ser setado ao primeiro usuário cadastrado a permissão de ROOT e após isso esse primeiro usuário já pode setar as permissões aos demais usuários.

Ao entrar no sistema o usuário deve receber uma mensagem de boas vindas informando suas permissões.
De acordo com suas permissões será as opções que ele deve ter disponível na tela.

Caso seja apenas consulta ele terá acesso a parte das estatísticas e a todo restante do sistema apenas como consulta, não podendo fazer alterações, iclusões ou qualquer outra ação que não seja consulta.

Se a permissão for criar, vai poder cadastrar produtos e clientes, e também emitir notas, além de poder ter acesso as estatísticas, porém não poderá alterar dados existentes, pois para isso é necessário a permissão de editar, com exceção de notas que ainda estejam com status pendente.

Se a permissão for editar, ele poderá apenas editar os registros e se for criar e editar vai poder criar e editar, mas não poderá desligar registros, pois para isso é necessário a permissão de excluir.

Se a permissão for excluir, então ele poderá também desligar registros, e se for criar, editar e excluir ele poderá fazer o CRUD completo, apenas não poderá setar permissões aos usuários, ou cadastrar funcionários, pois para isso é necessário a permissão de ROOT.

Caso o usuário tenha permissão de ROOT ele poderá setar as permissões para ele mesmo e os demais usuários, portanto 
se ele tiver a permissão de ROOT ele consegue fazer o que quiser no sistema.

Quanto aos registros de venda (notas fiscais):

Para emitir o registro de venda, o usuário seleciona o funcionário que efetuou a venda e o cliente que fez a compra, e em seguida ele é direcionado para a tela onde vai adicionar os itens vendidos, após adicionar todos os itens ele tem a opção de fechar a tela de emissão de notas, e com isso a nota ficaria com status de pendente, pois ela não foi emitida de fato, enquanto ela estiver pendente é considerado que a venda não se realizou ainda, e portanto o usuário pode entrar nela novamente, incluindo ou excluindo produtos, alterando dados da nota, após o usuário concluir ele deve emitir a nota, e com isso a nota passará pro status de emitida, e passará a constar como registro para as estatísticas, e a partir disso não será mais possível fazer nenhuma alteração na nota, a não ser o seu cancelamento (se o usuário tiver essa permissão). Ao cancelar a nota fiscal o seu status passa para cancelada, seu valor é zerado e ela automaticamente não é mais considerada nas estatísticas.

Quanto as estatísticas:

Esse, na minha opinião é o principal diferencial do sistema em relação ao sistema da oficina.
Ao entrar na seção das estatísticas o usuário deverá informar o período o qual ele deseja consultar, ao informar o intervalo de datas ele terá as seguintes opções de consulta:
- Ranking de vendas por cliente
- Ranking de vendas por funcionário
- Ranking de vendas por produto (com preço médio no intervalo consultado)

Outro diferencial em relação ao projeto da oficina, é a quantidade de opções de consultas de vendas.

Opções de consultas de vendas:
- Todas as notas
- Todas as notas emitidas
- Todas as notas pendentes
- Todas as notas canceladas
- Notas por data da venda
  - Todas as notas por data de venda
  - Notas emitidas por data de venda
  - Notas pendentes por data de venda
  - Notas canceladas por data de venda
- Notas por cliente
  - Todas as notas por cliente
  - Notas emitidas por cliente
  - Notas pendentes por cliente
  - Notas canceladas por cliente
- Notas por funcionário
  - Todas as notas por funcionário
  - Notas emitidas por funcionário
  - Notas pendentes por funcionário
  - Notas canceladas por funcionário
 

Em resumo, podemos ver que esse sistema já foi uma evolução em relação ao sistema da oficina, pois já possui uma complexidade considerável e grandes evoluções. Neste projeto consegui explorar bastante a linguagem SQL para fazer as consultas e as estatísticas do banco de dados, mas o que achei um pouco mais complexo de desenvolver é a lógica das vendas.

Também esse sistema foi super importante para exercitar a lógica de permissão, do que os usuários podem ou não podem fazer, dependendo de suas permissões, e também a lógica dos registros de vendas e dos dados para formação das estatísticas.

Quem quiser ver como ficou basta baixar esse projeto, e instalar as dependências (basicamente pyqt5) e o Python na versão 3.x

Para poder cadastrar um usuário e setar suas permissões deve utilizar inicialmente o superusuário ROOT e a senha manager.

Para executar o sistema utilize o arquivo padaria.py, que vai abrir a tela de login, onde você poderá logar com o superusuário ROOT, cadastrar um usuário, setar suas permissões e em seguida logar novamente com o usuário que você cadastrou e testar para ver como ficou esse meu segundo projeto do Jovem Programador Senac módulo 2.
