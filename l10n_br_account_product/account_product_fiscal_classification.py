# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2012  Renato Lima - Akretion                                  #
#                                                                             #
#This program is free software: you can redistribute it and/or modify         #
#it under the terms of the GNU Affero General Public License as published by  #
#the Free Software Foundation, either version 3 of the License, or            #
#(at your option) any later version.                                          #
#                                                                             #
#This program is distributed in the hope that it will be useful,              #
#but WITHOUT ANY WARRANTY; without even the implied warranty of               #
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
#GNU Affero General Public License for more details.                          #
#                                                                             #
#You should have received a copy of the GNU Affero General Public License     #
#along with this program.  If not, see <http://www.gnu.org/licenses/>.        #
###############################################################################

from openerp.osv import orm, fields

FC_SQL_CONSTRAINTS = [
        ('account_fiscal_classfication_code_uniq', 'unique (name)',
         u'Já existe um classificação fiscal com esse código!')
    ]


class AccountProductFiscalClassificationTemplate(orm.Model):
    _inherit = 'account.product.fiscal.classification.template'

    def _get_taxes(self, cr, uid, ids, name, arg, context=None):
        result = {}
        for fiscal_classification in self.browse(cr, uid, ids,
                                                 context=context):
            fc_id = fiscal_classification.id
            result[fc_id] = {'sale_base_tax_ids': [],
                             'purchase_base_tax_ids': []}
            sale_tax_ids = []
            purchase_tax_ids = []
            for line in fiscal_classification.sale_tax_definition_line:
                sale_tax_ids.append(line.tax_id.id)
            for line in fiscal_classification.purchase_tax_definition_line:
                purchase_tax_ids.append(line.tax_id.id)
            sale_tax_ids.sort()
            purchase_tax_ids.sort()
            result[fc_id]['sale_base_tax_ids'] = sale_tax_ids
            result[fc_id]['purchase_base_tax_ids'] = purchase_tax_ids
        return result

    _columns = {
        'type': fields.selection([('view', u'Visão'),
                                  ('normal', 'Normal'),
                                  ('extension', u'Extensão')], 'Tipo'),
        'parent_id': fields.many2one(
            'account.product.fiscal.classification.template',
            'Parent Fiscal Classification',
            domain="[('type', 'in', ('view', 'normal'))]", select=True),
        'child_ids': fields.one2many(
            'account.product.fiscal.classification.template',
             'parent_id', 'Child Fiscal Classifications'),
        'sale_tax_definition_line': fields.one2many(
            'l10n_br_tax.definition.sale.template',
            'fiscal_classification_id', 'Taxes Definitions'),
        'note': fields.text(u'Observações'),
        'inv_copy_note': fields.boolean(
            u'Copiar Observação',
            help=u"Copia a observação no documento fiscal"),
        'sale_base_tax_ids': fields.function(
            _get_taxes, method=True, type='many2many',
            relation='account.tax', string='Sale Taxes', multi='all'),
        'purchase_tax_definition_line': fields.one2many(
            'l10n_br_tax.definition.purchase.template',
            'fiscal_classification_id', 'Taxes Definitions'),
        'purchase_base_tax_ids': fields.function(
            _get_taxes, method=True, type='many2many',
            relation='account.tax', string='Purchase Taxes', multi='all'),
        'cest': fields.char(
            string='CEST', size=9,
            help=u"Código Especificador da Substituição Tributária "),
    }
    _defaults = {
        'type': 'normal'}
    _sql_constraints = FC_SQL_CONSTRAINTS


class L10n_brTaxDefinitionSaleTemplate(orm.Model):
    _name = 'l10n_br_tax.definition.sale.template'
    _inherit = 'l10n_br_tax.definition.template'
    _columns = {
        'fiscal_classification_id': fields.many2one(
            'account.product.fiscal.classification.template',
            'Fiscal Classification', select=True)
    }
    _sql_constraints = [
        ('l10n_br_tax_definition_tax_id_uniq', 'unique (tax_id,\
        fiscal_classification_id)',
        u'Imposto já existente nesta classificação fiscal!')
    ]


class L10n_brTaxDefinitionPurchaseTemplate(orm.Model):
    _name = 'l10n_br_tax.definition.purchase.template'
    _inherit = 'l10n_br_tax.definition.template'
    _columns = {
        'fiscal_classification_id': fields.many2one(
            'account.product.fiscal.classification.template',
            'Fiscal Classification', select=True)
    }
    _sql_constraints = [
        ('l10n_br_tax_definition_tax_id_uniq', 'unique (tax_id,\
        fiscal_classification_id)',
        u'Imposto já existente nesta classificação fiscal!')
    ]


class AccountProductFiscalClassification(orm.Model):
    _inherit = 'account.product.fiscal.classification'

    def name_get(self, cr, uid, ids, context=None):
        reads = self.read(cr, uid, ids, ['name','description', 'id'], context=context)
        res = []
        for record in reads:
            name =  "%s - %s" % (record['name'], record['description'])
            res.append((record['id'], name))
        return res

    def _get_taxes(self, cr, uid, ids, name, arg, context=None):
        result = {}
        for fiscal_classification in self.browse(cr, uid, ids,
                                                 context=context):
            fc_id = fiscal_classification.id
            result[fc_id] = {'sale_base_tax_ids': [],
                             'purchase_base_tax_ids': []}
            sale_tax_ids = []
            purchase_tax_ids = []
            for line in fiscal_classification.sale_tax_definition_line:
                sale_tax_ids.append(line.tax_id.id)
            for line in fiscal_classification.purchase_tax_definition_line:
                purchase_tax_ids.append(line.tax_id.id)
            sale_tax_ids.sort()
            purchase_tax_ids.sort()
            result[fc_id]['sale_base_tax_ids'] = sale_tax_ids
            result[fc_id]['purchase_base_tax_ids'] = purchase_tax_ids
        return result

    _columns = {
        'type': fields.selection([('view', u'Visão'),
                                  ('normal', 'Normal'),
                                  ('extension', 'Extensão')], 'Tipo'),
        'parent_id': fields.many2one(
            'account.product.fiscal.classification',
            'Parent Fiscal Classification',
            domain="[('type', 'in', ('view', 'normal'))]", select=True),
        'child_ids': fields.one2many('account.product.fiscal.classification',
                                     'parent_id',
                                     'Child Fiscal Classifications'),
        'sale_tax_definition_line': fields.one2many(
            'l10n_br_tax.definition.sale',
            'fiscal_classification_id', 'Taxes Definitions'),
        'note': fields.text(u'Observações'),
        'inv_copy_note': fields.boolean(
            u'Copiar Observação no Documento Fiscal'),
        'sale_base_tax_ids': fields.function(
            _get_taxes, method=True, type='many2many',
            relation='account.tax', string='Sale Taxes', multi='all'),
        'purchase_tax_definition_line': fields.one2many(
            'l10n_br_tax.definition.purchase',
            'fiscal_classification_id', 'Taxes Definitions'),
        'purchase_base_tax_ids': fields.function(
            _get_taxes, method=True, type='many2many',
            relation='account.tax', string='Purchase Taxes', multi='all'),
        'cest': fields.char(
            string='CEST', size=9,
            help=u"Código Especificador da Substituição Tributária "),
    }
    _defaults = {
        'type': 'normal'}
    _sql_constraints = FC_SQL_CONSTRAINTS

    def button_update_products(self, cr, uid, ids, context=None):

        result = True
        if not context:
            context = {}

        obj_product = self.pool.get('product.template')

        for fiscal_classification in self.browse(cr, uid, ids):
            product_ids = obj_product.search(
                cr, uid, [('ncm_id', '=', fiscal_classification.id)],
                context=context)

            current_company_id = self.pool.get('res.users').browse(
                cr, uid, uid).company_id.id

            for product in obj_product.browse(cr, uid, product_ids, context):
                to_keep_sale_tax_ids = self.pool.get('account.tax').search(
                    cr, uid, [('id', 'in', [x.id for x in product.taxes_id]),
                              ('company_id', '!=', current_company_id)])

                to_keep_purchase_tax_ids = self.pool.get('account.tax').search(
                    cr, uid, [('id', 'in', [x.id for x in product.supplier_taxes_id]),
                    ('company_id', '!=', current_company_id)])

                vals = {
                        'taxes_id': [(6, 0, list(set(to_keep_sale_tax_ids + [x.id for x in fiscal_classification.sale_base_tax_ids])))],
                        'supplier_taxes_id': [(6, 0, list(set(to_keep_purchase_tax_ids + [x.id for x in fiscal_classification.purchase_base_tax_ids])))],
                }

                obj_product.write(cr, uid, product.id, vals, context)

        return result


class L10n_brTaxDefinitionSale(orm.Model):
    _name = 'l10n_br_tax.definition.sale'
    _inherit = 'l10n_br_tax.definition'
    _columns = {
        'fiscal_classification_id': fields.many2one(
            'account.product.fiscal.classification',
            'Parent Fiscal Classification', select=True)
    }
    _sql_constraints = [
        ('l10n_br_tax_definition_tax_id_uniq', 'unique (tax_id,\
        fiscal_classification_id)',
        u'Imposto já existente nesta classificação fiscal!')
    ]


class L10n_brTaxDefinitionPurchase(orm.Model):
    _name = 'l10n_br_tax.definition.purchase'
    _inherit = 'l10n_br_tax.definition'
    _columns = {
                'fiscal_classification_id': fields.many2one(
                    'account.product.fiscal.classification',
                    'Fiscal Classification', select=True)
    }
    _sql_constraints = [
        ('l10n_br_tax_definition_tax_id_uniq', 'unique (tax_id,\
        fiscal_classification_id)',
        u'Imposto já existente nesta classificação fiscal!')]


class WizardAccountProductFiscalClassification(orm.TransientModel):
    _inherit = 'wizard.account.product.fiscal.classification'
    _columns = {
        'company_id': fields.many2one('res.company', 'Company')
    }

    def action_create(self, cr, uid, ids, context=None):

        obj_wizard = self.browse(cr, uid, ids[0])
        obj_tax = self.pool.get('account.tax')
        obj_company = self.pool.get('res.company')
        obj_tax_template = self.pool.get('account.tax.template')
        obj_tax_code = self.pool.get('account.tax.code')
        obj_tax_code_template = self.pool.get('account.tax.code.template')
        obj_fclass = self.pool.get('account.product.fiscal.classification')
        obj_fclass_template = self.pool.get(
            'account.product.fiscal.classification.template')
        obj_tax_purchase = self.pool.get('l10n_br_tax.definition.purchase')
        obj_tax_sale = self.pool.get('l10n_br_tax.definition.sale')

        if obj_wizard.company_id:
            company_ids = [obj_wizard.company_id.id]
        else:
            company_ids = obj_company.search(cr, uid, [])

        tax_template_ref = {}
        tax_code_template_ref = {}
        for company_id in company_ids:

            tax_template_ref[company_id] = {}
            tax_ids = obj_tax.search(cr, uid, [('company_id', '=', company_id)])
            for tax in obj_tax.browse(cr, uid, tax_ids):
                tax_template = obj_tax_template.search(
                    cr, uid, [('name', '=', tax.name)])
                if tax_template:
                    tax_template_ref[company_id][tax_template[0]] = tax.id

            tax_code_template_ref[company_id] = {}
            tax_code_ids = obj_tax_code.search(
                cr, uid, [('company_id', '=', company_id)])
            for tax_code in obj_tax_code.browse(cr, uid, tax_code_ids):
                tax_code_template = obj_tax_code_template.search(
                    cr, uid, [('name', '=', tax_code.name)])
                if tax_code_template:
                    tax_code_template_ref[company_id][tax_code_template[0]] = tax_code.id

        fclass_ids_template = obj_fclass_template.search(cr, uid, [])
        for fclass_template in obj_fclass_template.browse(cr, uid, fclass_ids_template):
            parent_ids = False
            parent_id = False
            for company_id in company_ids:
                vals = {
                        'name': fclass_template.name,
                        'description': fclass_template.description,
                        'type': fclass_template.type,
                        'parent_id': parent_id,
                        'cest': fclass_template.cest}
                if obj_wizard.company_id:
                    parent_ids = obj_fclass.search(cr, uid, [('name', '=', fclass_template.parent_id.name), ('company_id', '=', company_id)])
                    fclass = obj_fclass.search(cr, uid, [('name', '=', fclass_template.name), ('company_id', '=', company_id)])
                    vals['company_id'] = company_id
                else:
                    parent_ids = obj_fclass.search(cr, uid, [('name', '=', fclass_template.parent_id.name), ('company_id', '=', False)])
                    fclass = obj_fclass.search(cr, uid, [('name', '=', fclass_template.name), ('company_id', '=', False)])
                    vals['company_id'] = False

                if parent_ids:
                    parent_id = parent_ids[0]

                if not fclass:
                    new_fclass_id = obj_fclass.create(cr, uid, vals)
                else:
                    new_fclass_id = fclass[0]

                for sale_tax in fclass_template.sale_tax_definition_line:
                    if not obj_tax_sale.search(cr, uid, [('tax_id', '=', tax_template_ref[company_id].get(sale_tax.tax_id.id, False)), ('fiscal_classification_id', '=', new_fclass_id)]):
                        obj_tax_sale.create(cr, uid, {
                            'tax_id': tax_template_ref[company_id].get(sale_tax.tax_id.id, False),
                            'tax_code_id': tax_code_template_ref[company_id].get(sale_tax.tax_code_id.id, False),
                            'fiscal_classification_id': new_fclass_id})

                for purchase_tax in fclass_template.purchase_tax_definition_line:
                    if not obj_tax_purchase.search(cr, uid, [('tax_id', '=',tax_template_ref[company_id].get(purchase_tax.tax_id.id, False)), ('fiscal_classification_id', '=', new_fclass_id)]):
                        obj_tax_purchase.create(cr, uid, {
                            'tax_id': tax_template_ref[company_id].get(purchase_tax.tax_id.id, False),
                            'tax_code_id': tax_code_template_ref[company_id].get(purchase_tax.tax_code_id.id, False),
                            'fiscal_classification_id': new_fclass_id})
        return {}
