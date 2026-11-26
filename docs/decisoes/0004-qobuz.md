# 0004 — Qobuz como serviço de streaming

- **Status:** Aceita (2026-11-26, tarefa 3)
- **Complementa:** a lista de serviços do item 7 e da US10 de [requisitos.md](../requisitos.md) e o enum `service` do [plano.md §2](../plano.md#2-modelo-de-dados)

## Contexto
A lista original de serviços (Tidal, Spotify, Apple Music, Deezer, YouTube Music, Amazon Music, Bandcamp e "outro") não incluía o Qobuz, que o usuário usa. Na tarefa 3, o enum `Service` (`library/choices.py`) foi criado para o `User.preferred_service`, e o `StreamingLink` vai reaproveitá-lo na tarefa 9.

## Decisão
- `Service` ganha o valor `qobuz` (rótulo "Qobuz"), antes de `other`.
- Na tarefa 10, `detect_service` reconhece `qobuz.com`, `open.qobuz.com` e `play.qobuz.com`.

## Consequências
- ➕ O Qobuz pode ser o serviço preferido e ter um link próprio, com a regra de um link por serviço.
- Os links do Qobuz no MusicBrainz, se existirem, são importados pela D12 como qualquer outro serviço reconhecido. A cobertura real ainda precisa ser conferida nas fixtures da tarefa 12.
