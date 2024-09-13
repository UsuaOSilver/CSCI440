#include <linux/module.h>
#include <linux/init.h>
#include <linux/kernel.h>

#include <linux/fs.h>		 // for basic file system
#include <linux/proc_fs.h>	 // for the proc filesystem
#include <linux/seq_file.h>	 // for squence files
#include <linux/mm.h>

// Show method
static int numpagefaults_proc_show(struct seq_file *m, void *v)
{
	unsigned long numpgfaults[NR_VM_EVENT_ITEMS];

	all_vm_events(numpgfaults);
	unsigned long numpagefaults = numpgfaults[PGFAULT];

	seq_printf(m, "%lu\n", numpagefaults);
	
	return 0;
}


// Custom init & exit methods
static int __init proc_numpagefaults_init(void)
{
	proc_create_single("numpagefaults", 0, NULL, numpagefaults_proc_show);
	printk(KERN_INFO "numpagefaults loaded succesfully\n");
	return 0;
}

static void __exit proc_numpagefaults_exit(void)
{
	remove_proc_entry("numpagefaults", NULL);
	printk(KERN_INFO "Exiting kernel...");
}

module_init(proc_numpagefaults_init);
module_exit(proc_numpagefaults_exit);

// Module metadata
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Nhat Anh Nguyen");
MODULE_DESCRIPTION("A simple kernel module that prints statistic each time cat /proc/numpagefaults is called");

