
### Explicação do Código

O código utiliza o Selenium para automatizar a navegação na Amazon Brasil, coletando informações sobre livros relacionados à automação. Ele faz o seguinte:

1. **Inicializa o navegador Chrome** usando o `ChromeDriverManager`.
2. **Navega até a Amazon** e realiza uma pesquisa por "livros sobre automação".
3. **Coleta dados** dos primeiros 10 livros listados, incluindo título, autor, preço, nota de avaliação e número de avaliações.
4. **Salva os dados** em um arquivo Excel usando o Pandas.

### Como Usar

1. **Instale as dependências** necessárias com `pip install selenium pandas webdriver-manager`.
2. **Execute o script** com `python scraping_amazon.py`.
3. **Verifique o arquivo Excel** gerado (`livros_automacao.xlsx`) para ver os dados coletados.

### Considerações Finais

Este script de web scraping foi feito em 31/01/2025 a onde foi usado a estrutura da Amazon no momento, pode ocasionar mudanças futuramente 
