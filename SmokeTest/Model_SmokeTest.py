import torch

from Models.LatentGPT import LatentGPT

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def param_count(model: torch.nn.Module) -> int:
    return sum(p.numel() for p in model.parameters())

def main():
    VOCAB_SIZE = 32000
    MAX_SEQ_LEN = 32768
    NUM_HEADS = 4
    EMBED_DIM = 1792
    LATENT_DIM = 512
    MLP_DIM = 7168
    NUM_LAYERS = 24
    DROPOUT = 0.1

    model = LatentGPT(
        vocab_size=VOCAB_SIZE,
        max_seq_len=MAX_SEQ_LEN,
        embed_dim=EMBED_DIM,
        latent_dim=LATENT_DIM,
        mlp_dim=MLP_DIM,
        num_layers=NUM_LAYERS,
        dropout=DROPOUT,
        num_heads=NUM_HEADS
    ).to(device)

    model.eval()
    batch_size = 2
    input_ids = torch.randint(0, VOCAB_SIZE, (batch_size, MAX_SEQ_LEN), device=device)
    with torch.no_grad():
        logits = model(input_ids)
    assert logits.shape == (batch_size, MAX_SEQ_LEN, VOCAB_SIZE)
    print("Forward OK · logits", logits.shape)

    model.train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    targets = input_ids.clone()
    logits = model(input_ids)
    loss = torch.nn.functional.cross_entropy(
        logits.view(-1, VOCAB_SIZE), targets.view(-1)
    )
    loss.backward()
    optimizer.step()

    print(f"Backward OK · loss {loss.item():.4f}")
    print(f"Param count {param_count(model)/1e6:.1f}M")

if __name__ == "__main__":
    main()
