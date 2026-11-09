# Operação local e dados

Este projeto foi preparado para execução local e versionamento do código no GitHub. A API atual não tem autenticação; mantenha-a em `127.0.0.1` e não a exponha diretamente à internet com dados reais.

- Uploads têm limite de 10 MB e 10 mil vendas após deduplicação.
- O servidor guarda cada DataFrame em memória por **uma hora**. Uma consulta posterior limpa sessões expiradas.
- Reiniciar a API apaga as bases enviadas. Recarregar a página perde o identificador guardado no estado React; faça novo upload.
- O CSV de demonstração fica no repositório. Arquivos reais enviados pela interface não são gravados no disco nem versionados automaticamente.
- O frontend usa o proxy do Vite para acessar a API. Em produção futura, será necessário definir hospedagem, autenticação, limites de acesso e armazenamento apropriado.

Para diagnosticar erros, veja [problemas comuns](troubleshooting.md).
