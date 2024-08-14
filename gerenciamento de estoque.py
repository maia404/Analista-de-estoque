# Trabalho Prático 2

import json


class Node:
    def __init__(self, item, price, quantity=1, description="", barcode=""):
        self.item = item
        self.price = price
        self.quantity = quantity
        self.description = description
        self.barcode = barcode
        self.left = None
        self.right = None


class Estoque:
    def __init__(self):
        self.root = None

    def add(self, item, price, quantity=1, description="", barcode=""):
        new_node = Node(item, price, quantity, description, barcode)
        if not self.root:
            self.root = new_node
        else:
            self._add(self.root, new_node)
        print(f'O produto {item} com preço {price} foi adicionado ao estoque!')

    def _add(self, root, new_node):
        if new_node.item < root.item:
            if root.left is None:
                root.left = new_node
            else:
                self._add(root.left, new_node)
        else:
            if root.right is None:
                root.right = new_node
            else:
                self._add(root.right, new_node)

    def remove(self, item):
        self.root, deleted = self._remove(self.root, item)
        if deleted:
            print(f'O item {item} foi retirado!')
        else:
            print("Item não encontrado no estoque.")

    def _remove(self, root, item):
        if root is None:
            return root, False

        deleted = False
        if item < root.item:
            root.left, deleted = self._remove(root.left, item)
        elif item > root.item:
            root.right, deleted = self._remove(root.right, item)
        else:
            deleted = True
            if root.left is None:
                return root.right, deleted
            elif root.right is None:
                return root.left, deleted

            min_larger_node = self._find_min(root.right)
            root.item, root.price, root.quantity, root.description, root.barcode = (
                min_larger_node.item, min_larger_node.price, min_larger_node.quantity,
                min_larger_node.description, min_larger_node.barcode
            )
            root.right, _ = self._remove(root.right, min_larger_node.item)

        return root, deleted

    def _find_min(self, root):
        while root.left:
            root = root.left
        return root

    def exibir_estoque(self):
        if not self.root:
            print("Estoque está vazio")
        else:
            total_value, total_products = self._exibir_estoque(self.root)
            print(f'Valor total do estoque: {total_value:.2f}')
            print(f'Número total de produtos: {total_products}')

    def _exibir_estoque(self, root):
        total_value = 0
        total_products = 0
        if root:
            left_value, left_products = self._exibir_estoque(root.left)
            total_value += left_value
            total_products += left_products

            print(f'Produto: {root.item}, Preço: {
                  root.price:.2f}, Quantidade: {root.quantity}')
            total_value += root.price * root.quantity
            total_products += 1

            right_value, right_products = self._exibir_estoque(root.right)
            total_value += right_value
            total_products += right_products
        return total_value, total_products

    def save_to_file(self, filename):
        data = self._tree_to_list(self.root)
        with open(filename, 'w') as file:
            json.dump(data, file)

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        self.root = self._list_to_tree(data)

    def _tree_to_list(self, root):
        if not root:
            return None
        return {
            'item': root.item,
            'price': root.price,
            'quantity': root.quantity,
            'description': root.description,
            'barcode': root.barcode,
            'left': self._tree_to_list(root.left),
            'right': self._tree_to_list(root.right)
        }

    def _list_to_tree(self, data):
        if not data:
            return None
        node = Node(data['item'], data['price'], data['quantity'],
                    data['description'], data['barcode'])
        node.left = self._list_to_tree(data['left'])
        node.right = self._list_to_tree(data['right'])
        return node

    def search(self, item):
        return self._search(self.root, item)

    def _search(self, root, item):
        if root is None or root.item == item:
            return root
        if item < root.item:
            return self._search(root.left, item)
        return self._search(root.right, item)

    def update_quantity(self, item, quantity):
        node = self.search(item)
        if node:
            node.quantity = quantity
            print(f'A quantidade do item {
                  item} foi atualizada para {quantity}.')
        else:
            print("Item não encontrado no estoque.")

    def search_by_price(self, price):
        results = []
        self._search_by_price(self.root, price, results)
        return results

    def _search_by_price(self, root, price, results):
        if root:
            self._search_by_price(root.left, price, results)
            if root.price == price:
                results.append(root)
            self._search_by_price(root.right, price, results)

    def search_by_description(self, description):
        results = []
        self._search_by_description(self.root, description.lower(), results)
        return results

    def _search_by_description(self, root, description, results):
        if root:
            self._search_by_description(root.left, description, results)
            if description in root.description.lower():
                results.append(root)
            self._search_by_description(root.right, description, results)


def main():
    estoque = Estoque()

    while True:
        print("\n1. Adicionar estoque")
        print("2. Remover estoque")
        print("3. Mostrar estoque")
        print("4. Atualizar quantidade")
        print("5. Salvar estoque em arquivo")
        print("6. Carregar estoque de arquivo")
        print("7. Pesquisar por preço")
        print("8. Pesquisar por descrição")
        print("9. Sair")

        opcao = input("O que deseja realizar: ")

        if opcao == "1":
            item = input('Digite o nome do Item que deseja adicionar: ')
            price = float(input('Digite o preço do Item: '))
            quantity = int(input('Digite a quantidade do Item: '))
            description = input('Digite a descrição do Item: ')
            barcode = input('Digite o código de barras do Item: ')
            estoque.add(item, price, quantity, description, barcode)
        elif opcao == "2":
            estoque.exibir_estoque()
            item = input('Digite o nome do Item que deseja remover: ')
            estoque.remove(item)
        elif opcao == "3":
            print(f'Aqui está o estoque!')
            estoque.exibir_estoque()
        elif opcao == "4":
            item = input(
                'Digite o nome do Item que deseja atualizar a quantidade: ')
            quantity = int(input('Digite a nova quantidade do Item: '))
            estoque.update_quantity(item, quantity)
        elif opcao == "5":
            filename = input(
                'Digite o nome do arquivo para salvar o estoque: ')
            estoque.save_to_file(filename)
            print(f'Estoque salvo em {filename}!')
        elif opcao == "6":
            filename = input(
                'Digite o nome do arquivo para carregar o estoque: ')
            estoque.load_from_file(filename)
            print(f'Estoque carregado de {filename}!')
        elif opcao == "7":
            price = float(input('Digite o preço que deseja pesquisar: '))
            results = estoque.search_by_price(price)
            if results:
                print(f"Produtos encontrados com preço {price}:")
                for product in results:
                    print(f'Item: {product.item}, Preço: {product.price:.2f}, Quantidade: {
                          product.quantity}, Descrição: {product.description}')
            else:
                print(f"Nenhum produto encontrado com preço {price}.")
        elif opcao == "8":
            description = input('Digite a descrição que deseja pesquisar: ')
            results = estoque.search_by_description(description)
            if results:
                print(f"Produtos encontrados com descrição contendo '{
                      description}':")
                for product in results:
                    print(f'Item: {product.item}, Preço: {product.price:.2f}, Quantidade: {
                          product.quantity}, Descrição: {product.description}')
            else:
                print(f"Nenhum produto encontrado com descrição contendo '{
                      description}'.")
        elif opcao == "9":
            print("Finalizando!")
            break
        else:
            print("Opção inválida!")


if __name__ == '__main__':
    main()
