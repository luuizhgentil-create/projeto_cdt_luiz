import tkinter as tk
from tkinter import messagebox
import json

# =========================
# DADOS
# =========================
jogos = {
    "Minecraft": 120.0,
    "GTA V": 150.0,
    "FIFA 25": 300.0,
    "Call of Duty": 280.0,
    "Need for Speed": 200.0,
    "Fortnite": 0.0,
    "Roblox": 0.0,
}

carrinho = []
vendas = []

ARQUIVO_JSON = "vendas_jogos.json"

# =========================
# FUNÇÕES
# =========================
def atualizar_total():
    total = sum(item["preco"] for item in carrinho)
    label_total.config(text=f"Total: R$ {total:.2f}")


def adicionar():
    jogo = jogo_var.get()
    cliente = cliente_var.get().strip()

    if jogo == "Selecione um jogo":
        messagebox.showerror("Erro", "Selecione um jogo!")
        return

    if not cliente:
        messagebox.showerror("Erro", "Digite o nome do cliente!")
        return

    item = {
        "jogo": jogo,
        "preco": jogos[jogo]
    }

    carrinho.append(item)

    listbox.insert(tk.END, f"{jogo} - R$ {item['preco']:.2f}")
    atualizar_total()


def remover():
    if carrinho:
        carrinho.pop()
        listbox.delete(tk.END)
        atualizar_total()


def finalizar():
    if not carrinho:
        messagebox.showwarning("Aviso", "Carrinho vazio!")
        return

    cliente = cliente_var.get().strip()

    venda = {
        "cliente": cliente,
        "itens": carrinho.copy(),
        "total": sum(i["preco"] for i in carrinho)
    }

    vendas.append(venda)

    # 💾 SALVA AUTOMATICAMENTE
    salvar_json()

    messagebox.showinfo("Sucesso", "Compra finalizada e salva!")

    carrinho.clear()
    listbox.delete(0, tk.END)
    cliente_var.set("")
    atualizar_total()


def salvar_json():
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(vendas, f, indent=4, ensure_ascii=False)


def ver_vendas():
    if not vendas:
        messagebox.showinfo("Vendas", "Nenhuma venda registrada ainda.")
        return

    texto = ""
    for i, v in enumerate(vendas, start=1):
        texto += f"\nVenda {i}\nCliente: {v['cliente']}\nTotal: R$ {v['total']:.2f}\n"

    messagebox.showinfo("Histórico de Vendas", texto)


# =========================
# JANELA
# =========================
janela = tk.Tk()
janela.title("Loja de Jogos - UPGRADE")
janela.geometry("700x600")
janela.config(bg="#0f172a")

# Título
tk.Label(
    janela,
    text="🎮 LOJA DE JOGOS PRO",
    font=("Arial", 20, "bold"),
    bg="#0f172a",
    fg="#facc15"
).pack(pady=10)

# Cliente
tk.Label(janela, text="Cliente:", bg="#0f172a", fg="white").pack()
cliente_var = tk.StringVar()
tk.Entry(janela, textvariable=cliente_var, width=40).pack(pady=5)

# Jogo
tk.Label(janela, text="Jogo:", bg="#0f172a", fg="white").pack()
jogo_var = tk.StringVar(value="Selecione um jogo")
tk.OptionMenu(janela, jogo_var, *jogos.keys()).pack(pady=5)

# Botões
frame_btn = tk.Frame(janela, bg="#0f172a")
frame_btn.pack(pady=10)

tk.Button(frame_btn, text="Adicionar", command=adicionar).grid(row=0, column=0, padx=5)
tk.Button(frame_btn, text="Remover", command=remover).grid(row=0, column=1, padx=5)
tk.Button(frame_btn, text="Finalizar", command=finalizar).grid(row=0, column=2, padx=5)
tk.Button(frame_btn, text="Ver Vendas", command=ver_vendas).grid(row=0, column=3, padx=5)

# Lista
listbox = tk.Listbox(janela, width=70, height=12)
listbox.pack(pady=10)

# Total
label_total = tk.Label(
    janela,
    text="Total: R$ 0.00",
    font=("Arial", 14, "bold"),
    bg="#0f172a",
    fg="#facc15"
)
label_total.pack(pady=10)

janela.mainloop()