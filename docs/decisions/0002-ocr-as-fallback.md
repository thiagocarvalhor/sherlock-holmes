# Decisao 0002: OCR Como Fallback

## Contexto

OCR e caro, sensivel a qualidade do documento e pode introduzir erro de leitura.

## Decisao

OCR deve ser acionado apenas quando:

- o dado estruturado do PNCP nao basta;
- um documento oficial contem informacao necessaria;
- o documento nao tem texto extraivel;
- a revisao documental indicar necessidade.

## Consequencias

- a UI pode indicar que OCR talvez seja necessario;
- a UI nao precisa executar OCR agora;
- OCR deve gerar evidencia propria com nivel de confianca adequado;
- revisao humana continua necessaria para conclusoes sensiveis.
