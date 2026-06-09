# Decisão 0002: OCR Como Fallback

## Contexto

OCR é caro, sensível à qualidade do documento e pode introduzir erro de leitura.

## Decisão

OCR deve ser acionado apenas quando:

- o dado estruturado do PNCP não basta;
- um documento oficial contém informação necessária;
- o documento não tem texto extraível;
- a revisão documental indica necessidade.

## Consequências

- a UI pode indicar que OCR talvez seja necessário;
- a UI não precisa executar OCR agora;
- OCR deve gerar evidência própria com nível de confiança adequado;
- revisão humana continua necessária para conclusões sensíveis.
