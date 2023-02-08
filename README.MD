<h1 align="center"> Draw-Project </h1>

<p align="center">
<img src="http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge"/>
</p>

<h2> Descrição </h2>

<p>
O projeto é um blog/rede social que da espaço para os usuários postarem suas artes e interagirem com as artes de outros
usuários, como comentar, dar like e seguir seus artistas favoritos. Ele também conta com sistema de autenticação de usuários
(cadastro e login), edição de perfil com descrição (bio) e imagem de usuário, visualização de perfil de outros usuários e 
um CRUD para suas próprias publicações.
</p>

<h2> Features </h2>

<ul>
<li>Publicar suas artes</li>
<li>Seguir outros usuários</li>
<li>Curtir e comentar posts</li>
<li>Editar seu perfil e posts</li>
</ul>

<h2> Screenshots </h2>

![Imagem da home page](https://user-images.githubusercontent.com/95861523/215090261-db7623e9-9549-42bf-a10c-ed362805b58d.png)

![Imagem da detail view e funções como like e comentários](https://user-images.githubusercontent.com/95861523/215090285-3686d1d7-fe81-4f39-9123-705470184f1b.png)

![Feed e perfil](https://user-images.githubusercontent.com/95861523/215090291-84180c7d-5a1d-4df7-9d3b-2782edbf174d.png)


<h2> Tecnologias utilizadas </h2>

<ul>
<li>Python</li>
<li>Django</li>
<li>Django Rest Framework</li>
<li>HTML</li>
<li>CSS</li>
<li>Javascript e Ajax (mínimo)</li>
</ul>

<h2> Rodando o projeto </h2>
<h4> Dependências </h4>
<ul>
<li>Python 3.0 ou +</li>
</ul>
<h4> Clonando o projeto </h4>

```
git clone git@github.com:mga98/draw-project.git
```

<h4> Configurando o projeto </h4>
<p> Abra o terminal com o ambiente virtual ativo e execute os seguintes comandos: </p>

```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
pytest ou python manage.py test # Para executar os testes da aplicação
python manage.py runserver
```
