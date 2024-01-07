from flask import Flask, render_template_string, request, jsonify
from datetime import datetime

app = Flask(__name__)

historico_vendas = []
vendas_totais = {'total': 0.0}

@app.route('/')
def index():
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vendas Da Rebeca</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond&display=swap');
            
            :root {
            }

            * {
                font-family: 'Cormorant Garamond', serif;
                font-size: 20px;
            }

            body {
                background-color: #ffffff;
                display: flex;
                justify-content: center;
                align-items: center;
                text-align: center;
            }

            .container {
                background-color: #ada4a4;
                width: 500px;
                margin: auto;
                padding: 20px;
                border-radius: 40px;
            }

            .container h2 {
                text-align: center;
                font-size: 2.5rem;
            }

            .vendas-container {
                margin-top: 20px;
                text-align: left;
            }

            .div-logotipo {
                width: 100%;
                heigth: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .logotipo{
                border-radius: 50%;
                width: 50%;
                heigth: 50%;
            }

            .vendas-container {
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="div-logotipo"><img class="logotipo" src="{{ url_for('static', filename='logotipo.jpg') }}" alt="Logotipo"></div>

            <h2>Vendas Da Rebeca</h2>

            <div>
                <form id="registrar_venda_form" method="post">
                    <input type="radio" name="produto" value="Empadão 250g" checked> Empadão 250g - €4,00<br>
                    <input type="radio" name="produto" value="Empadão 500g"> Empadão 500g - €7,00<br><br>
                    Quantidade: <input type="text" name="quantidade" id="quantidade" required>
                    <input type="button" value="Registrar Venda" onclick="registrarVenda()">
                </form>
            </div>
            
            <div class="vendas-container" id="vendas_do_dia_container"></div>

            <div class="vendas-container">
                <h3>Resumo de Vendas</h3>
                <p>Vendas Do Dia: €<span id="vendas_do_dia_total">{{ vendas_totais['do_dia'] }}</span></p>
                <p>Vendas Totais: €<span id="vendas_totais">{{ vendas_totais['total'] }}</span></p>
            </div>

            <div class="vendas-container">
                <h3>Histórico de Vendas</h3>
                <select id="historico_select" onchange="mostrarVendasPorDia(this.value)">
                    {% for historico in historico_vendas %}
                        <option value="{{ historico['data'] }}">{{ historico['data'] }}</option>
                    {% endfor %}
                </select>
                <button onclick="verVendasAnteriores()">Ver Vendas Anteriores</button>
                <div id="vendas_por_dia_container"></div>
            </div>
        </div>

        <script>
            function registrarVenda() {
                var form = document.getElementById('registrar_venda_form');
                var formData = new FormData(form);

                var xhr = new XMLHttpRequest();
                xhr.open('POST', '/registrar_venda', true);
                xhr.onload = function () {
                    if (xhr.status === 200) {
                        mostrarVendasDoDia();
                        mostrarResumoVendas();
                    } else {
                        console.error('Erro ao registrar a venda.');
                    }
                };
                xhr.send(formData);
            }

            function mostrarVendasDoDia() {
                var container = document.getElementById('vendas_do_dia_container');
                container.innerHTML = '';

                var xhr = new XMLHttpRequest();
                xhr.open('GET', '/vendas_do_dia', true);
                xhr.onload = function () {
                    if (xhr.status === 200) {
                        try {
                            var vendas_do_dia = JSON.parse(xhr.responseText);
                            if (vendas_do_dia.length > 0) {
                                var ul = document.createElement('ul');
                                for (var i = 0; i < vendas_do_dia.length; i++) {
                                    var li = document.createElement('li');
                                    li.innerHTML = vendas_do_dia[i]['produto'] + ' - Quantidade: ' + vendas_do_dia[i]['quantidade'] + ' - Preço: €' + vendas_do_dia[i]['preco'] + ' - Data: ' + vendas_do_dia[i]['data_venda'];
                                    ul.appendChild(li);
                                }
                                container.appendChild(ul);
                            } else {
                                container.innerHTML = 'Nenhuma venda registrada hoje.';
                            }
                        } catch (error) {
                            console.error('Erro ao processar as vendas do dia:', error);
                        }
                    } else {
                        console.error('Erro ao obter as vendas do dia.');
                    }
                };
                xhr.send();
            }

            function mostrarResumoVendas() {
                var xhr = new XMLHttpRequest();
                xhr.open('GET', '/resumo_vendas', true);
                xhr.onload = function () {
                    if (xhr.status === 200) {
                        var resumo_vendas = JSON.parse(xhr.responseText);
                        document.getElementById('vendas_do_dia_total').innerText = resumo_vendas['do_dia'];
                        document.getElementById('vendas_totais').innerText = resumo_vendas['total'];
                    } else {
                        console.error('Erro ao obter o resumo de vendas.');
                    }
                };
                xhr.send();
            }

            function mostrarVendasPorDia(data) {
                var container = document.getElementById('vendas_por_dia_container');
                container.innerHTML = '';

                var xhr = new XMLHttpRequest();
                xhr.open('GET', '/vendas_por_dia?data=' + data, true);
                xhr.onload = function () {
                    if (xhr.status === 200) {
                        try {
                            var vendas_por_dia = JSON.parse(xhr.responseText);
                            if (vendas_por_dia.length > 0) {
                                var ul = document.createElement('ul');
                                for (var i = 0; i < vendas_por_dia.length; i++) {
                                    var li = document.createElement('li');
                                    li.innerHTML = vendas_por_dia[i]['produto'] + ' - Quantidade: ' + vendas_por_dia[i]['quantidade'] + ' - Preço: €' + vendas_por_dia[i]['preco'] + ' - Data: ' + vendas_por_dia[i]['data_venda'];
                                    ul.appendChild(li);
                                }
                                container.appendChild(ul);
                            } else {
                                container.innerHTML = 'Nenhuma venda registrada nesta data.';
                            }
                        } catch (error) {
                            console.error('Erro ao processar as vendas por dia:', error);
                        }
                    } else {
                        console.error('Erro ao obter as vendas por dia.');
                    }
                };
                xhr.send();
            }

            mostrarVendasDoDia();
            mostrarResumoVendas();  // Exibir resumo de vendas ao carregar a página

            function verVendasAnteriores() {
                var dataSelecionada = document.getElementById('historico_select').value;
                mostrarVendasPorDia(dataSelecionada);
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(template, vendas_totais=vendas_totais, historico_vendas=historico_vendas)

@app.route('/registrar_venda', methods=['POST'])
def registrar_venda():
    produto = request.form.get('produto')
    quantidade = int(request.form.get('quantidade'))

    if produto == 'Empadão 250g':
        preco = 4.0
    elif produto == 'Empadão 500g':
        preco = 7.0
    else:
        preco = 0.0

    valor_venda = preco * quantidade
    data_venda = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    vendas_do_dia = {'produto': produto, 'preco': preco, 'quantidade': quantidade, 'data_venda': data_venda}
    vendas_totais['total'] += valor_venda

    if not any(venda['data'] == data_venda[:10] for venda in historico_vendas):
        historico_vendas.append({'data': data_venda[:10], 'vendas_do_dia': [vendas_do_dia], 'vendas_totais': vendas_totais['total']})
    else:
        for historico in historico_vendas:
            if historico['data'] == data_venda[:10]:
                historico['vendas_do_dia'].append(vendas_do_dia)
                historico['vendas_totais'] = vendas_totais['total']

    return 'OK'

@app.route('/vendas_do_dia')
def obter_vendas_do_dia():
    for historico in reversed(historico_vendas):
        if historico['data'] == datetime.now().strftime('%Y-%m-%d'):
            return jsonify(historico['vendas_do_dia'])
    return jsonify([])

@app.route('/vendas_por_dia')
def obter_vendas_por_dia():
    data = request.args.get('data')
    for historico in reversed(historico_vendas):
        if historico['data'] == data:
            return jsonify(historico['vendas_do_dia'])
    return jsonify([])

@app.route('/resumo_vendas')
def obter_resumo_vendas():
    resumo_vendas = {'do_dia': 0.0, 'total': vendas_totais['total']}
    for historico in reversed(historico_vendas):
        if historico['data'] == datetime.now().strftime('%Y-%m-%d'):
            resumo_vendas['do_dia'] = historico['vendas_totais']
            break
    return jsonify(resumo_vendas)

if __name__ == '__main__':
    app.run(debug=True)
