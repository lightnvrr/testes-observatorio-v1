# Base Lattes: KatieNet / Observatório de Mulheres na Ciência

Pipeline que baixa, consolida e gera indicadores da base Lattes (Painel Formação e Atuação Lattes, CNPq) para o observatório. A metodologia completa está em [docs/metodologia_lattes.md](docs/metodologia_lattes.md).

## Instalação (Windows, PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

No VS Code, selecione o interpretador `.venv` (Ctrl+Shift+P, "Python: Select Interpreter"). Os testes aparecem no painel de testes.

## Uso

```powershell
python scripts/baixar_lattes.py --anos 2020-2026   # brutos em data/raw/ + manifest.json
python scripts/consolidar_lattes.py                # data/processed/lattes_consolidado.csv
python scripts/gerar_indicadores.py                # data/processed/indicadores/
python scripts/gerar_indicadores.py --sem-negra    # sem a categoria Negra (Preta + Parda)
```

### Saídas dos indicadores

Em `data/processed/indicadores/`:

- `indicadores_v1.csv`: formato longo, uma linha por indicador × base × período × recorte × categoria × sexo × raça, com numerador, denominador, percentual (0 a 100), linhas de auditoria e as flags `flag_denominador_pequeno`, `flag_numerador_pequeno` e `flag_preferir_agregado`.
- `indicadores_dicionario.csv`: nomes, definições e ressalvas de cada indicador, base temporal e recorte (para os rótulos do front).
- `indicadores_v1.meta.json`: extração, parâmetros (categoria Negra, limites das flags) e SHA-256 do consolidado.
- `qualidade_v1.csv`: taxas de "Não informado" e notas de qualidade, para a metodologia (não é para o público).

### Download dos brutos

O painel do CNPq embute um workbook do Tableau Public. O script baixa a exportação CSV da aba "Painel - Download", um ano por vez (cerca de 50 s e 20 MB por ano), com pausa entre anos.

- Destino: `data/raw/{data_extracao}/lattes_{ano}.csv`, guardado exatamente como veio, com `manifest.json` na mesma pasta (URL, data do download, tamanho, SHA-256, linhas, pessoas e a data de extração original).
- Se o arquivo já existe e confere com o manifest, o ano é pulado. `--force` baixa de novo; se o CNPq tiver feito uma extração nova, ela vai para outra pasta.
- Opções: `--anos 2020-2026` ou `--anos 2020,2023`, `--timeout`, `--tentativas`, `--espera`, `--pausa` (veja `--help`).
- Se a automação falhar, o script mostra como baixar à mão. Os arquivos baixados à mão vão para `data/raw/_entrada/lattes_{ano}.csv` e são validados e organizados na próxima execução.

## Testes

```powershell
pytest            # só unitários (sem dados reais)
pytest -m dados   # conferência com os dados reais (exige data/raw/ preenchido)
pytest -m rede    # verifica se o painel do CNPq está acessível
```
